import argparse
import sys
import os
import json
import requests
from sbol import *
from synbiohub_adapter.query_synbiohub import SynBioHubQuery
from synbiohub_adapter.SynBioHubUtil import SD2Constants
from pySBOLx.pySBOLx import Experiment


def main(args=None):
    if args is None:
        args = sys.argv[1:]

    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input_files', nargs='*', default=[
                        f for f in os.listdir('.') if os.path.isfile(f) and f.endswith('.xml')])
    parser.add_argument('-c', '--collection_uri', nargs='?',
                        default=SD2Constants.SD2_DESIGN_COLLECTION)
    parser.add_argument('-b', '--sub_collection_uris', nargs='*', default=[])
    parser.add_argument('-w', '--overwrite', action='store_true')
    parser.add_argument('-u', '--url', nargs='?',
                        default='https://hub.sd2e.org')
    parser.add_argument('-e', '--email', nargs='?',
                        default='sd2_service@sd2e.org')
    parser.add_argument('-p', '--password')
    parser.add_argument('-s', '--sparql', nargs='?',
                        default='http://hub-api.sd2e.org:80/sparql')
    parser.add_argument('-l', '--locked_predicates', nargs='*', default=[])
    args = parser.parse_args(args)

    docs = load_documents(args.input_files)

    sbh = SynBioHub(args.url, args.email, args.password,
                    args.sparql, set(args.locked_predicates))

    for doc in docs:
        sbh.submit_to_collection(
            doc, args.collection_uri, args.overwrite, args.sub_collection_uris)


def load_documents(sbol_files):
    docs = []
    for sbol_file in sbol_files:
        doc = Document()
        doc.read(sbol_file)
        docs.append(doc)
    return docs


class SynBioHub():

    def __init__(self, url, email, password, sparql, locked_predicates=set()):
        self.url = url
        self.part_shop = PartShop(url + '/')
        self.part_shop.login(email, password)
        response = requests.post(
            url + '/login', headers={'Accept': 'text/plain'}, data={'email': email, 'password': password})
        self.token = response.content.decode('UTF-8')
        self.sparql = sparql
        self.locked_predicates = locked_predicates

    def attach_file(self, file, uri):
        response = requests.post(uri + '/attach', headers={'Accept': 'text/plain', 'X-authorization': self.token}, files={'file': open(file, 'rb')})

        print('attached file')
        print(response)

    # for a given plan URI, retrieve its intent JSON
    def get_plan_intent_attachment(self, plan_uri):

        sbh_query = SynBioHubQuery(self.sparql)
        attachments = sbh_query.query_plan_attachments(plan_uri)
        for binding in attachments['results']['bindings']:
            response = requests.get(binding['attachment_id']['value'] + '/download', headers={'Accept': 'text/plain', 'X-authorization': self.token})
            attachment_json = response.json()
            # TODO find a better way to identify intent attachments
            if attachment_json.get("experimental-variables") != None:
                return attachment_json

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

        if len(self.query_collection_members([plan_uri], [SD2Constants.SD2_EXPERIMENT_COLLECTION], 'http://sd2e.org#Experiment')) == 0:
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

        self.part_shop.submit(doc, SD2Constants.SD2_EXPERIMENT_COLLECTION, 2)

        print('pushed plan parameter')
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

        print('pushed sample parameter')
        print(response)  

    def submit_to_collection(self, doc, collection_uri, overwrite, sub_collection_uris=[]):
        Config.setOption('validate', False)
        Config.setOption('sbol_typed_uris', False)

        local_to_remote = self.__map_local_to_remote(
            doc, collection_uri, sub_collection_uris)

        print('mapped local to remote')

        if overwrite or len(local_to_remote) == 0:
            if len(local_to_remote) > 0:
                if len(self.locked_predicates) > 0:
                    self.__copy_remote_predicates(doc, local_to_remote)
                self.remove_all(local_to_remote.values())

                print('removed remote')

            response = self.part_shop.submit(doc, collection_uri, 2)

            print('submitted local')
            print(response)
        else:
            print(repr(local_to_remote.keys())[
                  10:-1] + ' have been previously uploaded and would be overwritten. Upload aborted. To overwrite, include -w in arguments.')

    def search_sub_collections(self, collection_uri):
        sub_collection_uris = []

        results = json.loads(
            self.part_shop.searchSubCollections(collection_uri))
        for result in results:
            sub_collection_uris.append(result['uri'])

        return sub_collection_uris

    def query_sub_collection_members(self, member_uris, collection_uri):
        sub_collection_uris = self.search_sub_collections(collection_uri)

        if len(sub_collection_uris) > 0:
            return self.query_collection_members(member_uris, sub_collection_uris)
        else:
            return {}

    def query_collection_members(self, member_uris, collection_uris=[], rdf_type=None):
        responses = []

        cut_len = 50
        sbh_query = SynBioHubQuery(self.sparql)
        if len(member_uris) <= cut_len:
            responses.append(sbh_query.query_collection_members(
                collection_uris, member_uris, rdf_type))
        else:
            cut_i = []
            for i in range(0, len(member_uris) // cut_len + 1):
                cut_i.append(i * cut_len)
            cut_i.append(cut_i[-1] + len(member_uris) % cut_len)
            for i in range(0, len(cut_i) - 1):
                responses.append(sbh_query.query_collection_members(
                    collection_uris, member_uris[cut_i[i]:cut_i[i + 1]], rdf_type))

        collection_to_member = {}

        for response in responses:
            for binding in response['results']['bindings']:
                if len(collection_uris) == 1:
                    collection_uri = collection_uris[0]
                else:
                    collection_uri = binding['collection']['value']
                try:
                    collection_to_member[collection_uri].append(
                        binding['entity']['value'])
                except:
                    try:
                        collection_to_member[collection_uri] = [
                            binding['entity']['value']]
                    except:
                        pass

        return collection_to_member

    def remove_all(self, uris):
        header = {'Accept': 'text/plain', 'X-authorization': self.token}
        for uri in uris:
            requests.get(uri + '/remove', headers=header)

    def __map_local_to_remote(self, doc, collection_uri, sub_collection_uris):
        remote_namespace = '/'.join(collection_uri.split('/')[:-2])
        setHomespace(remote_namespace.replace('https', 'http'))

        remote_to_local = {}
        for local_entity in doc:
            remote_to_local['/'.join([remote_namespace, local_entity.identity.split(
                '/')[-2], '1'])] = local_entity.identity

        sub_collections = []
        for sub_collection_uri in sub_collection_uris:
            uri_arr = sub_collection_uri.split('/')
            sub_collection = Collection(uri_arr[-2], uri_arr[-1])
            sub_collections.append(sub_collection)

            for local_entity in doc:
                sub_collection.members = sub_collection.members + \
                    [local_entity.identity]

        for sub_collection in sub_collections:
            doc.addCollection(sub_collection)

        sub_collection_to_remote = self.query_sub_collection_members(
            list(remote_to_local.keys()), collection_uri)

        local_to_remote = {}
        if len(sub_collection_to_remote) == 0:
            collection_to_remote = self.query_collection_members(
                list(remote_to_local.keys()), [collection_uri])
            for collection_key in collection_to_remote.keys():
                for remote_uri in collection_to_remote[collection_key]:
                    local_to_remote[remote_to_local[remote_uri]] = remote_uri
        else:
            for sub_collection_uri in sub_collection_to_remote:
                uri_arr = sub_collection_uri.split('/')
                sub_collection = Collection(uri_arr[-2], uri_arr[-1])
                try:
                    doc.addCollection(sub_collection)

                    for remote_uri in sub_collection_to_remote[sub_collection_uri]:
                        sub_collection.members = sub_collection.members + \
                            [remote_to_local[remote_uri]]
                except:
                    pass

                for remote_uri in sub_collection_to_remote[sub_collection_uri]:
                    local_to_remote[remote_to_local[remote_uri]] = remote_uri

        return local_to_remote

    def __copy_remote_predicates(self, doc, local_to_remote):
        setHomespace(self.url + '/')

        for local_uri in local_to_remote:
            local_entity = doc.getTopLevel(local_uri)

            remote_doc = Document()
            self.part_shop.pull(local_to_remote[local_uri], remote_doc)
            remote_entity = remote_doc.getTopLevel(local_to_remote[local_uri])

            remote_predicates = [
                p for p in remote_entity.getProperties() if p in self.locked_predicates]

            for remote_predicate in remote_predicates:
                setattr(local_entity, remote_predicate, URIProperty(
                    local_entity.this, remote_predicate, '0', '*'))

            for remote_predicate in remote_predicates:
                for obj in remote_entity.getPropertyValues(remote_predicate):
                    local_entity.addPropertyValue(remote_predicate, obj)


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
