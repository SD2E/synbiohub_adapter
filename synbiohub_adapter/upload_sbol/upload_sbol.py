import argparse
import sys
import os
import json
import requests
import re
from urllib3.exceptions import HTTPError
from sbol import *
from synbiohub_adapter import SynBioHubQuery
from synbiohub_adapter import SD2Constants


def main(args=None):
    if args is None:
        args = sys.argv[1:]

    parser = argparse.ArgumentParser()
    parser.add_argument('-e', '--email')
    parser.add_argument('-p', '--password')
    parser.add_argument('-u', '--url', nargs='?', default='https://hub.sd2e.org')
    parser.add_argument('-s', '--sparql', nargs='?', default='http://hub-api.sd2e.org:80/sparql')
    parser.add_argument('-f', '--sbol_files', nargs='*',
                        default=[f for f in os.listdir('.') if os.path.isfile(f) and f.endswith('.xml')])
    parser.add_argument('-w', '--overwrite', action='store_true')
    parser.add_argument('-W', '--overwrite_sub_collections', action='store_true')
    parser.add_argument('-c', '--collection_uri', nargs='?', default=None)
    parser.add_argument('-i', '--sub_collection_id', nargs='?', default=None)
    parser.add_argument('-n', '--sub_collection_name', nargs='?', default=None)
    parser.add_argument('-d', '--sub_collection_description', nargs='?', default=None)
    parser.add_argument('-v', '--sub_collection_version', nargs='?', default='1')
    parser.add_argument('-I', '--collection_id', nargs='?', default=None)
    parser.add_argument('-N', '--collection_name', nargs='?', default=None)
    parser.add_argument('-D', '--collection_description', nargs='?', default=None)
    parser.add_argument('-V', '--collection_version', nargs='?', default='1')
    parser.add_argument('-m', '--max_upload', nargs='?', default='0')

    args = parser.parse_args(args)

    Config.setOption('sbol_typed_uris', False)
    setHomespace(SD2Constants.ADAPTER_NS)

    docs = []

    for sbol_file in args.sbol_files:
        docs.append(Document())
        docs[-1].read(sbol_file)

    if len(docs) > 0:
        sbh = SynBioHub(args.url, args.email, args.password, args.sparql)

        if (args.collection_id is not None and args.collection_version is not None and args.collection_name
                is not None and args.collection_description is not None):
            sbh.submit_collection(docs[0], args.collection_id, args.collection_version, args.collection_name,
                                  args.collection_description, int(args.max_upload))
        elif args.collection_uri is not None:
            sbh.submit_to_collection(docs, args.collection_uri, int(args.max_upload), args.overwrite,
                                     args.overwrite_sub_collections, args.sub_collection_id,
                                     args.sub_collection_version, args.sub_collection_name,
                                     args.sub_collection_description)
        else:
            raise CollectionArgumentError()
    else:
        raise EmptySubmissionError()


class SynBioHub():
    def __init__(self, url, email, password, sparql, spoofed_url=None):
        url = url.rstrip('/')
        self.url = url
        self.email = email
        self.part_shop = PartShop(url)
        self.part_shop.login(email, password)
        response = requests.post(url + '/login',
                                 headers={'Accept': 'text/plain'},
                                 data={'email': email, 'password': password})
        self.token = response.content.decode('UTF-8')
        self.sparql = sparql
        self.spoofed_url = spoofed_url

    def __resubmit_collection(self, doc, collection_id, overwrite):
        if overwrite:
            if self.spoofed_url:
                collection_uri = '/'.join([self.spoofed_url, 'user', self.email, collection_id,
                                          collection_id + '_collection', '1'])
            else:
                collection_uri = '/'.join([self.url, 'user', self.email, collection_id,
                                          collection_id + '_collection', '1'])

            response = self.part_shop.submit(doc, collection_uri, 1)

            print(response)
        else:
            raise DuplicateCollectionError(doc.displayId, doc.version)

    def submit_collection(self, doc, collection_id, collection_version, collection_name, collection_description,
                          max_upload=0, sub_collection_id=None, sub_collection_version=None,
                          sub_collection_name=None, sub_collection_description=None, overwrite=False):
        if max_upload > 0 and len(doc) > max_upload:
            raise MaxUploadError(max_upload)

        if sub_collection_id is not None and sub_collection_version is not None:
            self.__create_root_sub_collection(doc, sub_collection_id, sub_collection_version, sub_collection_name,
                                              sub_collection_description)

        doc.displayId = collection_id
        doc.name = collection_name
        doc.description = collection_description
        doc.version = collection_version

        try:
            response = self.part_shop.submit(doc)

            print(response)
        # If Collection already exists on SynBioHub, then DuplicateCollectionError should be raised unless overwriting.
        # Since exception raised by PartShop in this case is generic, currently check its message.
        except RuntimeError as e:
            if str(e).endswith('Submission id and version already in use'):
                if overwrite:
                    self.__resubmit_collection(doc, collection_id, overwrite)
                else:
                   raise DuplicateCollectionError(doc.displayId, doc.version) 
            else:
                raise e
        except HTTPError as e:
            if e.reason.endswith('Submission id and version already in use'):
                if overwrite:
                    self.__resubmit_collection(doc, collection_id, overwrite)
                else:
                   raise DuplicateCollectionError(doc.displayId, doc.version) 
            else:
                raise e

    def submit_to_collection(self, docs, collection_uri, max_upload=0, overwrite=False,
                             overwrite_sub_collections=False, sub_collection_id=None, sub_collection_version=None,
                             sub_collection_name=None, sub_collection_description=None):
        collection_namespace = self.__get_top_level_namespace(collection_uri)

        submission_docs = []

        for doc in docs:
            if max_upload > 0 and len(doc) > max_upload or len(self.__get_namespaces(doc)) > 1:
                submission_docs = submission_docs + self.__split_document_by_namespace(doc, collection_namespace,
                                                                                       max_upload)

                submission_docs = submission_docs + self.__create_sub_collection_documents(doc, collection_namespace)
            else:
                submission_docs.append(doc)

        if sub_collection_id is not None and sub_collection_version is not None:
            submission_docs.append(self.__create_root_sub_collection_document(docs, collection_namespace,
                                                                              sub_collection_id,
                                                                              sub_collection_version,
                                                                              sub_collection_name,
                                                                              sub_collection_description))

        if overwrite and not overwrite_sub_collections:
            self.__merge_remote_sub_collections(submission_docs, collection_namespace)

        i = 0

        for submission_doc in submission_docs:
            i = i + 1

            try:
                if overwrite:
                    response = self.part_shop.submit(submission_doc, collection_uri, 3)
                else:
                    response = self.part_shop.submit(submission_doc, collection_uri, 2)

                print(response)
                print(repr(i) + ' of ' + repr(len(submission_docs)))
            except RuntimeError as e:
                if 'Submission id and version does not exist' in repr(e):
                    raise MissingCollectionError(collection_uri)
                elif not overwrite:
                    matched = re.match(r'Submission terminated\.\nA submission with this id already exists, and it \
includes an object: (.+) that is already in this repository and has different content', repr(e))

                    if matched is not None:
                        obj_uri_arr = matched.group(1).split('/')

                        raise ObjectMismatchError(obj_uri_arr[-2], obj_uri_arr[-1])

    @classmethod
    def __get_namespaces(cls, doc):
        namespaces = set()

        for obj in doc:
            namespaces.add(cls.__get_top_level_namespace(obj.identity))

        return namespaces

    @classmethod
    def __get_top_level_namespace(cls, uri):
        return '/'.join(uri.split('/')[:-2])

    @classmethod
    def __get_child_namespace(cls, uri):
        return '/'.join(uri.split('/')[:-3])

    @classmethod
    def __split_document_by_namespace(cls, doc, collection_namespace, split_cap=-1):
        namespace_to_docs = {}

        for seq in doc.sequences:
            copy_seq = cls.__copy_by_namespace(seq, namespace_to_docs, split_cap)

            cls.__port_reference_namespaces(copy_seq, 'attachments', doc, collection_namespace)
            cls.__port_reference_namespaces(copy_seq, 'wasDerivedFrom', doc, collection_namespace)
            cls.__port_reference_namespaces(copy_seq, 'wasGeneratedBy', doc, collection_namespace)

        for comp_def in doc.componentDefinitions:
            copy_comp_def = cls.__copy_by_namespace(comp_def, namespace_to_docs, split_cap)

            cls.__port_sub_reference_namespaces(copy_comp_def, 'components', 'definition', doc, collection_namespace)
            cls.__port_sub_sub_reference_namespaces(copy_comp_def, 'components', 'mapsTos', 'remote', doc,
                                                    collection_namespace)

            cls.__port_reference_namespaces(copy_comp_def, 'sequences', doc, collection_namespace)
            cls.__port_reference_namespaces(copy_comp_def, 'attachments', doc, collection_namespace)
            cls.__port_reference_namespaces(copy_comp_def, 'wasDerivedFrom', doc, collection_namespace)
            cls.__port_reference_namespaces(copy_comp_def, 'wasGeneratedBy', doc, collection_namespace)

        for derivation in doc.combinatorialderivations:
            copy_derivation = cls.__copy_by_namespace(derivation, namespace_to_docs, split_cap)

            cls.__port_sub_reference_namespaces(copy_derivation, 'variableComponents', 'variable', doc,
                                                collection_namespace)
            cls.__port_sub_reference_namespaces(copy_derivation, 'variableComponents', 'variants', doc,
                                                collection_namespace)
            cls.__port_sub_reference_namespaces(copy_derivation, 'variableComponents', 'variantCollections', doc,
                                                collection_namespace)
            cls.__port_sub_reference_namespaces(copy_derivation, 'variableComponents', 'variantDerivations', doc,
                                                collection_namespace)

            cls.__port_reference_namespaces(copy_derivation, 'template', doc, collection_namespace)

        for model in doc.models:
            copy_model = cls.__copy_by_namespace(model, namespace_to_docs, split_cap)

            cls.__port_reference_namespaces(copy_model, 'attachments', doc, collection_namespace)
            cls.__port_reference_namespaces(copy_model, 'wasDerivedFrom', doc, collection_namespace)
            cls.__port_reference_namespaces(copy_model, 'wasGeneratedBy', doc, collection_namespace)

        for mod_def in doc.moduleDefinitions:
            copy_mod_def = cls.__copy_by_namespace(mod_def, namespace_to_docs, split_cap)

            cls.__port_sub_reference_namespaces(copy_mod_def, 'modules', 'definition', doc, collection_namespace)
            cls.__port_sub_reference_namespaces(copy_mod_def, 'functionalComponents', 'definition', doc,
                                                collection_namespace)
            cls.__port_sub_sub_reference_namespaces(copy_mod_def, 'modules', 'mapsTos', 'remote', doc,
                                                    collection_namespace)
            cls.__port_sub_sub_reference_namespaces(copy_mod_def, 'functionalComponents', 'mapsTos', 'remote', doc,
                                                    collection_namespace)

            cls.__port_reference_namespaces(copy_mod_def, 'models', doc, collection_namespace)
            cls.__port_reference_namespaces(copy_mod_def, 'attachments', doc, collection_namespace)
            cls.__port_reference_namespaces(copy_mod_def, 'wasDerivedFrom', doc, collection_namespace)
            cls.__port_reference_namespaces(copy_mod_def, 'wasGeneratedBy', doc, collection_namespace)

        for imp in doc.implementations:
            copy_imp = cls.__copy_by_namespace(imp, namespace_to_docs, split_cap)

            cls.__port_reference_namespaces(copy_imp, 'built', doc, collection_namespace)
            cls.__port_reference_namespaces(copy_imp, 'attachments', doc, collection_namespace)
            cls.__port_reference_namespaces(copy_imp, 'wasDerivedFrom', doc, collection_namespace)
            cls.__port_reference_namespaces(copy_imp, 'wasGeneratedBy', doc, collection_namespace)

        for attach in doc.attachments:
            copy_attach = cls.__copy_by_namespace(attach, namespace_to_docs, split_cap)

            cls.__port_reference_namespaces(copy_attach, 'attachments', doc, collection_namespace)
            cls.__port_reference_namespaces(copy_attach, 'wasDerivedFrom', doc, collection_namespace)
            cls.__port_reference_namespaces(copy_attach, 'wasGeneratedBy', doc, collection_namespace)

        # for exp_datum in doc.experimentalData:
        #     copy_exp_datum = cls.__copy_by_namespace(exp_datum, namespace_to_docs, split_cap)

        #     cls.__port_reference_namespaces(copy_exp_datum, 'attachments', doc, collection_namespace)
        #     cls.__port_reference_namespaces(copy_exp_datum, 'wasDerivedFrom', doc, collection_namespace)
        #     cls.__port_reference_namespaces(copy_exp_datum, 'wasGeneratedBy', doc, collection_namespace)

        # for exp in doc.experiments:
        #     copy_exp = cls.__copy_by_namespace(exp, namespace_to_docs, split_cap)

        #     cls.__port_reference_namespaces(copy_exp, 'experimentalData', doc, collection_namespace)
        #     cls.__port_reference_namespaces(copy_exp, 'attachments', doc, collection_namespace)
        #     cls.__port_reference_namespaces(copy_exp, 'wasDerivedFrom', doc, collection_namespace)
        #     cls.__port_reference_namespaces(copy_exp, 'wasGeneratedBy', doc, collection_namespace)

        for agent in doc.agents:
            copy_agent = cls.__copy_by_namespace(agent, namespace_to_docs, split_cap)

            cls.__port_reference_namespaces(copy_agent, 'attachments', doc, collection_namespace)
            cls.__port_reference_namespaces(copy_agent, 'wasDerivedFrom', doc, collection_namespace)
            cls.__port_reference_namespaces(copy_agent, 'wasGeneratedBy', doc, collection_namespace)

        for plan in doc.plans:
            copy_plan = cls.__copy_by_namespace(plan, namespace_to_docs, split_cap)

            cls.__port_reference_namespaces(copy_plan, 'attachments', doc, collection_namespace)
            cls.__port_reference_namespaces(copy_plan, 'wasDerivedFrom', doc, collection_namespace)
            cls.__port_reference_namespaces(copy_plan, 'wasGeneratedBy', doc, collection_namespace)

        for act in doc.activities:
            copy_act = cls.__copy_by_namespace(act, namespace_to_docs, split_cap)

            cls.__port_sub_reference_namespaces(copy_act, 'usages', 'entity', doc, collection_namespace)
            cls.__port_sub_reference_namespaces(copy_act, 'associations', 'agent', doc, collection_namespace)
            cls.__port_sub_reference_namespaces(copy_act, 'associations', 'plan', doc, collection_namespace)

            cls.__port_reference_namespaces(copy_act, 'wasInformedBy', doc, collection_namespace)
            cls.__port_reference_namespaces(copy_act, 'attachments', doc, collection_namespace)
            cls.__port_reference_namespaces(copy_act, 'wasDerivedFrom', doc, collection_namespace)
            cls.__port_reference_namespaces(copy_act, 'wasGeneratedBy', doc, collection_namespace)

        split_docs = []

        for namespace in namespace_to_docs:
            split_docs = split_docs + namespace_to_docs[namespace]

        return split_docs

    @classmethod
    def __copy_by_namespace(cls, obj, namespace_to_docs, split_cap=-1):
        obj_namespace = cls.__get_top_level_namespace(obj.identity)

        if obj_namespace not in namespace_to_docs:
            namespace_to_docs[obj_namespace] = [Document()]
        elif split_cap > 0 and len(namespace_to_docs[obj_namespace][-1]) >= split_cap:
            namespace_to_docs[obj_namespace].append(Document())

        return obj.copy(namespace_to_docs[obj_namespace][-1])

    @classmethod
    def __port_reference_namespaces(cls, obj, property_name, doc, collection_namespace):
        if isinstance(obj, TopLevel):
            obj_namespace = cls.__get_top_level_namespace(obj.identity)
        else:
            obj_namespace = cls.__get_child_namespace(obj.identity)

        refs = getattr(obj, property_name)

        if isinstance(refs, list):
            static_refs = set()

            for ref in refs:
                if doc.getTopLevel(ref) is None:
                    static_refs.add(ref)
                else:
                    ref_namespace = cls.__get_top_level_namespace(ref)

                    if ref_namespace == obj_namespace or ref_namespace == collection_namespace:
                        static_refs.add(ref)

            if len(static_refs) != len(refs):
                refs = [ref if ref in static_refs else '/'.join([collection_namespace] + ref.split('/')[-2:])
                        for ref in refs]

                setattr(obj, property_name, refs)
        elif refs is not None:
            ref = refs

            ref_namespace = cls.__get_top_level_namespace(ref)

            if doc.getTopLevel(ref) is None or ref_namespace != obj_namespace and ref_namespace != collection_namespace:
                setattr(obj, property_name, '/'.join([collection_namespace] + ref.split('/')[-2:]))

    @classmethod
    def __port_sub_reference_namespaces(cls, obj, property_name, sub_property_name, doc, collection_namespace):
        for sub_obj in getattr(obj, property_name):
            cls.__port_reference_namespaces(sub_obj, sub_property_name, doc, collection_namespace)

    @classmethod
    def __port_sub_sub_reference_namespaces(cls, obj, property_name, sub_property_name, sub_sub_property_name, doc,
                                            collection_namespace):
        for sub_obj in getattr(obj, property_name):
            cls.__port_sub_reference_namespaces(sub_obj, sub_property_name, sub_sub_property_name, doc,
                                                collection_namespace)

    @classmethod
    def __create_sub_collection_documents(cls, doc, collection_namespace):
        sub_collection_docs = []

        for sub_collection in doc.collections:
            sub_collection_docs.append(Document())

            sub_copy = sub_collection.copy(sub_collection_docs[-1])

            sub_copy.members = ['/'.join([collection_namespace] + member.split('/')[-2:])
                                for member in sub_copy.members]

        return sub_collection_docs

    def __merge_remote_sub_collections(self, docs, collection_namespace):
        temp_homespace = getHomespace()
        setHomespace('')

        for doc in docs:
            remote_doc = Document()

            for sub_collection in doc.collections:
                remote_uri = '/'.join([collection_namespace, sub_collection.displayId, sub_collection.version])

                if self.spoofed_url:
                    pull_uri = remote_uri.replace(self.spoofed_url, self.url)
                else:
                    pull_uri = remote_uri

                try:
                    self.part_shop.pull(pull_uri, remote_doc, False)

                    try:
                        remote_sub_collection = remote_doc.getCollection(remote_uri)

                        sub_collection.members = sub_collection.members + remote_sub_collection.members
                    except RuntimeError as e:
                        raise SubCollectionMergeError(sub_collection.displayId, sub_collection.version, str(e))

                # If sub-Collection does not already exist on SynBioHub, then there is nothing to merge.
                except LookupError:
                    pass

        setHomespace(temp_homespace)

    @classmethod
    def __create_root_sub_collection_document(cls, docs, collection_namespace, sub_collection_id,
                                              sub_collection_version, sub_collection_name=None,
                                              sub_collection_description=None):
        root_sub_collection = cls.__create_sub_collection(sub_collection_id, sub_collection_version,
                                                          sub_collection_name, sub_collection_description)

        for doc in docs:
            remote_uri_arr = ['/'.join([collection_namespace] + obj.identity.split('/')[-2:]) for obj in doc]

            root_sub_collection.members = root_sub_collection.members + remote_uri_arr

        root_sub_collection_doc = Document()

        root_sub_collection_doc.addCollection(root_sub_collection)

        return root_sub_collection_doc

    @classmethod
    def __create_root_sub_collection(cls, doc, sub_collection_id, sub_collection_version, sub_collection_name=None,
                                     sub_collection_description=None):
        root_sub_collection = cls.__create_sub_collection(sub_collection_id, sub_collection_version,
                                                          sub_collection_name, sub_collection_description)

        local_uri_arr = [obj.identity for obj in doc]

        root_sub_collection.members = root_sub_collection.members + local_uri_arr

        doc.addCollection(root_sub_collection)

        return root_sub_collection

    @classmethod
    def __create_sub_collection(cls, sub_collection_id, sub_collection_version, sub_collection_name=None,
                                sub_collection_description=None):
        sub_collection = Collection(sub_collection_id, sub_collection_version)

        if sub_collection_name is not None:
            sub_collection.name = sub_collection_name
        else:
            sub_collection.name = sub_collection_id

        if sub_collection_description is not None:
            sub_collection.description = sub_collection_description

        return sub_collection

    def remove_all_identified(self, uris):
        header = {'Accept': 'text/plain', 'X-authorization': self.token}
        for uri in uris:
            requests.get(uri + '/remove', headers=header)

    def attach_file(self, file, uri):
        response = requests.post(uri + '/attach',
                                 headers={'Accept': 'text/plain',
                                          'X-authorization': self.token},
                                 files={'file': open(file, 'rb')})

        print(response)

    def query_collection_members(self, member_uris=[], collection_uris=[], rdf_type=None):
        responses = []

        cut_len = 50

        sbh_query = SynBioHubQuery(self.sparql, user=self.email, authentication_key=self.token,
                                   spoofed_url=self.spoofed_url)

        if len(member_uris) <= cut_len:
            responses.append(sbh_query.query_collection_members(collection_uris, member_uris, rdf_type))
        else:
            cut_i = []
            for i in range(0, len(member_uris) // cut_len + 1):
                cut_i.append(i * cut_len)
            cut_i.append(cut_i[-1] + len(member_uris) % cut_len)
            for i in range(0, len(cut_i) - 1):
                responses.append(sbh_query.query_collection_members(collection_uris,
                                                                    member_uris[cut_i[i]:cut_i[i + 1]],
                                                                    rdf_type))

        collection_to_member = {}

        for response in responses:
            for binding in response['results']['bindings']:
                if len(collection_uris) == 1:
                    collection_uri = collection_uris[0]
                else:
                    collection_uri = binding['collection']['value']

                if collection_uri not in collection_to_member:
                    collection_to_member[collection_uri] = []

                if 'entity' in binding:
                    collection_to_member[collection_uri].append(binding['entity']['value'])

        return collection_to_member

    # for a given plan URI, retrieve the named attachment
    def get_single_experiment_attachment(self, plan_uri, attachment_name):
        sbh_query = SynBioHubQuery(self.sparql)
        attachments = sbh_query.query_single_experiment_attachment(plan_uri, attachment_name)
        if len(attachments['results']['bindings']) > 0:
            attachment_id = attachments['results']['bindings'][0]['attachment_id']['value']
            response = requests.get(attachment_id + '/download',
                                    headers={'Accept': 'text/plain',
                                             'X-authorization': self.token})
            return response.json()
        print("No attachment found {}".format(attachment_name))

    # for a given plan URI, retrieve its intent JSON
    def get_single_experiment_intent_attachment(self, plan_uri):
        sbh_query = SynBioHubQuery(self.sparql)
        attachments = sbh_query.query_single_experiment_attachments(plan_uri)
        for binding in attachments['results']['bindings']:
            attachment_id = binding['attachment_id']['value']
            response = requests.get(attachment_id + '/download',
                                    headers={'Accept': 'text/plain',
                                             'X-authorization': self.token})
            try:
                attachment_json = response.json()
                # TODO find a better way to identify intent attachments
                if attachment_json.get("experimental-variables") is not None:
                    return attachment_json
            except ValueError:
                print("{} is not JSON, trying next attachment".format(attachment_id))

    def push_lab_plan_parameter(self, plan_uri, parameter_uri, parameter_value):
        """Pushes a lab parameter for a plan to SynBioHub.

        :param plan_uri: the URI for the plan.
        :param parameter_uri: the URI for the parameter to be attached to the plan.
        :param parameter_value: the value of the parameter to be set.
        :raises: BadLabParameterError, UndefinedURIError
        """
        try:
            assert parameter_uri in SD2Constants.PLAN_PARAMETER_PREDICATES
        except AssertionError:
            raise BadLabParameterError(parameter_uri)

        if len(self.query_collection_members([plan_uri],
                                             [SD2Constants.SD2_EXPERIMENT_COLLECTION],
                                             'http://sd2e.org#Experiment')) == 0:
            raise UndefinedURIError(plan_uri)

        uri_arr = plan_uri.split('/')

        Config.setOption('validate', False)
        Config.setOption('sbol_typed_uris', False)
        remote_namespace = '/'.join(uri_arr[:-2])
        setHomespace(remote_namespace.replace('https', 'http'))

        doc = Document()

        plan = Experiment(uri_arr[-2], version=uri_arr[-1])
        doc.addExtensionObject(plan)

        setattr(plan, parameter_uri, URIProperty(
            plan.this, parameter_uri, '0', '*'))
        plan.addPropertyValue(parameter_uri, parameter_value)

        response = self.part_shop.submit(doc, SD2Constants.SD2_EXPERIMENT_COLLECTION, 2)

        print(response)

    def push_lab_sample_parameter(self, sample_uri, parameter_uri, parameter_value):
        """Pushes a lab parameter for a sample to SynBioHub.

        :param sample_uri: the URI for the sample.
        :param parameter_uri: the URI for the parameter to be attached to the sample.
        :param parameter_value: the value of the parameter to be set.
        :raises: BadLabParameterError, UndefinedURIError
        """
        try:
            assert parameter_uri in SD2Constants.SAMPLE_PARAMETER_PREDICATES
        except AssertionError:
            raise BadLabParameterError(parameter_uri)

        collection_to_member = self.query_collection_members(
            [sample_uri], rdf_type='http://sbols.org/v2#Implementation')

        if len(collection_to_member) == 0:
            raise UndefinedURIError(sample_uri)

        uri_arr = sample_uri.split('/')

        Config.setOption('validate', False)
        Config.setOption('sbol_typed_uris', False)
        remote_namespace = '/'.join(uri_arr[:-2])
        setHomespace(remote_namespace.replace('https', 'http'))

        doc = Document()

        sample = Implementation(uri_arr[-2], uri_arr[-1])
        doc.addImplementation(sample)

        setattr(sample, parameter_uri, URIProperty(
            sample.this, parameter_uri, '0', '*'))
        sample.addPropertyValue(parameter_uri, parameter_value)

        response = self.part_shop.submit(doc, list(collection_to_member.keys())[0], 2)

        print(response)


class CollectionArgumentError(Exception):

    def __init__(self):
        pass

    def __str__(self):
        msg = ("Either the URI of an existing collection (-c) or the ID (-I),"
               " version (-V), name (-N), and description (-D) of a new"
               " collection must be provided as arguments.")
        return msg


class EmptySubmissionError(Exception):

    def __init__(self):
        pass

    def __str__(self):
        return "No documents were submitted for upload."


class MaxUploadError(Exception):

    def __init__(self, max_upload):
        self.max_upload = max_upload

    def __str__(self):
        msg = "Submitted document contains more objects than the max upload size of {max}"
        return msg.format(max=repr(self.max_upload))


class SubCollectionMergeError(Exception):

    def __init__(self, collection_id, collection_version, additional_detail=None):
        self.collection_id = collection_id
        self.collection_version = collection_version
        self.additional_detail = additional_detail

    def __str__(self):
        if self.additional_detail:
            msg = "Sub collection with ID {id} and version {ve} failed to merge. {ad}"

            return msg.format(id=self.collection_id, ve=self.collection_version, ad=self.additional_detail)
        else:
            msg = "Sub collection with ID {id} and version {ve} failed to merge."

            return msg.format(id=self.collection_id, ve=self.collection_version)


class MissingCollectionError(Exception):

    def __init__(self, collection_uri):
        self.collection_uri = collection_uri

    def __str__(self):
        return "There is no Collection with URI {uri}.".format(uri=self.collection_uri)


class DuplicateCollectionError(Exception):

    def __init__(self, collection_id, collection_version):
        self.collection_id = collection_id
        self.collection_version = collection_version

    def __str__(self):
        msg = "There already exists a Collection with ID {id} and version {ve}."
        return msg.format(id=self.collection_id, ve=self.collection_version)


class ObjectMismatchError(Exception):

    def __init__(self, obj_id, obj_version):
        self.obj_id = obj_id
        self.obj_version = obj.version

    def __str__(self):
        msg = "Target Collection already contains a non-matching object with ID {id} and version {ve}."
        return msg.format(id=self.obj_id, ve=obj_version)


class SBHLabParameterError(Exception):
    pass


class BadLabParameterError(SBHLabParameterError):

    def __init__(self, parameter):
        self.parameter = parameter

    def __str__(self):
        return "Invalid parameter URI: {}".format(self.parameter)


class UndefinedURIError(SBHLabParameterError):

    def __init__(self, uri):
        self.uri = uri

    def __str__(self):
        return "Undefined URI: {}".format(self.uri)


if __name__ == '__main__':
    main()
