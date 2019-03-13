import getpass
import sys
import csv

from SPARQLWrapper import SPARQLWrapper, JSON, POST
from sbol import *
from .cache_query import wrap_query_fn
from functools import partial

'''
    This is a utility module containing classes with constant variables used for querying SynBioHub information

    author(s) : Nicholas Roehner
                Tramy Nguyen
'''
class SBOLConstants():
    PRIMER = "http://identifiers.org/so/SO:0000112"
    RIBOSWITCH = "http://identifiers.org/so/SO:0000035"

    CHEMICAL_ENTITY = "http://identifiers.org/chebi/CHEBI:24431"
    EFFECTOR = "http://identifiers.org/chebi/CHEBI:35224"
    FLUORESCEIN = "http://identifiers.org/chebi/CHEBI:31624"
    H2O = "http://identifiers.org/chebi/CHEBI:15377"

    LOGIC_OPERATOR = "http://edamontology.org/data_2133"

    BEAD = "http://purl.obolibrary.org/obo/NCIT_C70671"
    BUFFER = "http://purl.obolibrary.org/obo/NCIT_C70815"
    CONTROL = "http://purl.obolibrary.org/obo/NCIT_C28143"
    FLUORESCENCE = "http://purl.obolibrary.org/obo/NCIT_C16586"
    NCIT_MEDIA = "http://purl.obolibrary.org/obo/NCIT_C85504"
    SOLUTION = "http://purl.obolibrary.org/obo/NCIT_C70830"
    STAIN = "http://purl.obolibrary.org/obo/NCIT_C841"
    NCIT_STRAIN = "http://purl.obolibrary.org/obo/NCIT_C14419"

    OBI_MEDIA = "http://purl.obolibrary.org/obo/OBI_0000079"
    OBI_STRAIN = "http://purl.obolibrary.org/obo/OBI_0001185"

    SBOL_NS = "http://sbols.org/v2#"
    OM_NS = 'http://www.ontology-of-units-of-measure.org/resource/om-2#'
    BBN_HOMESPACE = "https://synbiohub.bbn.com"

class BBNConstants():
    BBN_SERVER = "https://synbiohub.bbn.com/"
    BBN_YEASTGATES_COLLECTION = "https://synbiohub.bbn.com/user/tramyn/BBN_YEAST_GATES/BBN_YEAST_GATES_collection/1"
    BBN_RULE30_COLLECTION = 'https://synbiohub.bbn.com/user/tramyn/transcriptic_rule_30_q0_1_09242017/transcriptic_rule_30_q0_1_09242017_collection/1'

class SD2Constants():
    SD2_SERVER = "https://hub.sd2e.org"
    SD2_STAGING_SERVER = "https://hub-staging.sd2e.org"

    SD2_DESIGN_COLLECTION = 'https://hub.sd2e.org/user/sd2e/design/design_collection/1'
    RULE_30_DESIGN_COLLECTION = 'https://hub.sd2e.org/user/sd2e/design/rule_30/1'
    YEAST_GATES_DESIGN_COLLECTION = 'https://hub.sd2e.org/user/sd2e/design/yeast_gates/1'
    YEAST_GATES_STRAINS_COLLECTION = 'https://hub.sd2e.org/user/sd2e/design/yeast_gates_strains/1'
    RIBOSWITCHES_DESIGN_COLLECTION = 'https://hub.sd2e.org/user/sd2e/design/Riboswitches/1'
    NOVEL_CHASSIS_DESIGN_COLLECTION = 'https://hub.sd2e.org/user/sd2e/design/novel_chassis/1'

    SD2_EXPERIMENT_COLLECTION = 'https://hub.sd2e.org/user/sd2e/experiment/experiment_collection/1'
    RULE_30_EXPERIMENT_COLLECTION = 'https://hub.sd2e.org/user/sd2e/experiment/rule_30/1'
    YEAST_GATES_EXPERIMENT_COLLECTION = 'https://hub.sd2e.org/user/sd2e/experiment/yeast_gates/1'

    # SD2 labs
    GINKGO = 'Ginkgo'
    BIOFAB = 'BioFAB'
    TRANSCRIPTIC = 'Transcriptic'

    LUDOX = 'https://hub.sd2e.org/user/sd2e/design/ludox_S40/1'

    # Flow ETL
    # Link from plan_uri
    FLOW_POSITIVE_CONTROL = 'http://sd2e.org#positive_control'
    FLOW_POSITIVE_CONTROL_CHANNEL_CONFIG = 'http://sd2e.org#positive_control_channel_config'
    FLOW_NEGATIVE_CONTROL = 'http://sd2e.org#negative_control'
    FLOW_BEAD_CONTROL = 'http://sd2e.org#bead_control'

    PLAN_PARAMETER_PREDICATES = {
        FLOW_POSITIVE_CONTROL,
        FLOW_POSITIVE_CONTROL_CHANNEL_CONFIG,
        FLOW_NEGATIVE_CONTROL,
        FLOW_BEAD_CONTROL
    }

    # Runtime parameters, link from sample_uri
    FLOW_BEAD_MODEL = 'http://sd2e.org#bead_model'
    FLOW_BEAD_BATCH = 'http://sd2e.org#bead_batch'

    SAMPLE_PARAMETER_PREDICATES = {
        FLOW_BEAD_MODEL,
        FLOW_BEAD_BATCH
    }

    # bandpass/longpass channel configuration
    CYTOMETER_CHANNEL_EW = 'http://sd2e.org#cytometer_channel_excitation_wavelength'
    CYTOMETER_CHANNEL_EM_FILTER_TYPE = 'http://sd2e.org#cytometer_channel_emission_filter_type'
    CYTOMETER_CHANNEL_EM_FILTER_CENTER = 'http://sd2e.org#cytometer_channel_emission_filter_center'
    CYTOMETER_CHANNEL_EM_FILTER_WIDTH = 'http://sd2e.org#cytometer_channel_emission_filter_width'
    CYTOMETER_CHANNEL_FILTER_CUTOFF = 'http://sd2e.org#cytometer_channel_emission_filter_cutoff'

    # PR ETL, link from plan_uri
    PR_LUDOX_CONTROL = 'http://sd2e.org#platereader_LUDOX_control'
    PR_WATER_CONTROL = 'http://sd2e.org#platereader_water_control'
    PR_FLUORESCEIN_CONTROL = 'http://sd2e.org#platereader_fluorescein_control'

    LOGIC_OPERATORS = [
        "http://www.openmath.org/cd/logic1#not",
        "http://www.openmath.org/cd/logic1#or",
        "http://www.openmath.org/cd/logic1#xor",
        "http://www.openmath.org/cd/logic1#nor",
        "http://www.openmath.org/cd/logic1#xnor",
        "http://www.openmath.org/cd/logic1#and",
        "http://www.openmath.org/cd/logic1#nand",
        "http://www.openmath.org/cd/logic1#implies"
    ]

    ADAPTER_NS = 'http://hub.sd2e.org/adapter'

# class SBHConstants():
#     SD2_SERVER = "http://hub-api.sd2e.org:80/sparql"
#     BBN_SERVER = "https://synbiohub.bbn.com/"
#     BBN_YEASTGATES_COLLECTION = "https://synbiohub.bbn.com/user/tramyn/BBN_YEAST_GATES/BBN_YEAST_GATES_collection/1"
#     BBN_RULE30_COLLECTION = 'https://synbiohub.bbn.com/user/tramyn/transcriptic_rule_30_q0_1_09242017/transcriptic_rule_30_q0_1_09242017_collection/1'
#     RULE_30_EXPERIMENT_COLLECTION = 'https://hub.sd2e.org/user/sd2e/experiment/rule_30/1'
#     YEAST_GATES_EXPERIMENT_COLLECTION = 'https://hub.sd2e.org/user/sd2e/experiment/yeast_gates/1'
#     RULE_30_DESIGN_COLLECTION = 'https://hub.sd2e.org/user/sd2e/design/rule_30/1'
#     YEAST_GATES_DESIGN_COLLECTION = 'https://hub.sd2e.org/user/sd2e/design/yeast_gates/1'
#     SD2_DESIGN_COLLECTION = 'https://hub.sd2e.org/user/sd2e/design/design_collection/1'
#     SD2_EXPERIMENT_COLLECTION = 'https://hub.sd2e.org/user/sd2e/experiment/experiment_collection/1'

class SBOLQuery():
    ''' This class structures SPARQL queries for objects belonging to classes from the SBOL data model.
        An instance of this class will allow a user to pull information on these objects from the specified instance of SynBioHub.
    '''

    # server: The SynBioHub server to call sparql queries on.
    def __init__(self, server, use_fallback_cache=False, user=None, authentication_key=None, spoofed_url=None):
        self._server = server
        self._use_fallback_cache = use_fallback_cache
        self.user = user
        self.authentication_key = authentication_key
        self.spoofed_url = spoofed_url

        # If using fallback cache, wrap the fetch_SPARQL function
        # with cache storage/retrieval.
        if use_fallback_cache:
            self.fetch_SPARQL = wrap_query_fn(self.fetch_SPARQL)


    def login(self, user, password):
        if not '/sparql' in self._server:
            self._server += '/sparql'
        p = self._server.find('/sparql')
        resource = self._server[:p]
        login_endpoint = SPARQLWrapper(resource + '/login')
        login_endpoint.setMethod(POST)
        login_endpoint.addCustomHttpHeader('Content-Type', 'application/x-www-form-urlencoded')
        login_endpoint.addCustomHttpHeader('Accept', 'text/plain')
        login_endpoint.addCustomHttpHeader('charset', 'utf-8"')
        login_endpoint.addParameter('email', user)
        login_endpoint.addParameter('password', password)
        self.user = user
        self.authentication_key = login_endpoint.query().response.read().decode("utf-8")

    def fetch_SPARQL(self, server, query):
        sparql = SPARQLWrapper(self._server)
        if self.authentication_key and self.user:
            sparql.addCustomHttpHeader('X-authorization', self.authentication_key)
            if 'WHERE' in query:
                if self.spoofed_url:
                    resource = self.spoofed_url
                else:
                    resource = self._server
                if '/sparql' in resource:
                    p = resource.find('/sparql')
                    resource = resource[:p]
                FROM = "  FROM <{resource}/user/{user}> ".format(resource=resource, user=self.user)
                p = query.find('WHERE')
                query = query[:p] + FROM + query[p:]
        sparql.setQuery(query)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        return results

    # Constructs a partial SPARQL query for all collection members with
    # at least one of the specified types (or all of the specified types).
    def construct_type_pattern(self, types, all_types=True, entity_label='entity', type_label='type'):
        if len(types) == 0:
            return ""
        elif all_types or len(types) == 1:
                return "?{el} sbol:type {ty} .".format(ty=self.serialize_objects(types), el=entity_label)
        else:
            return """
            VALUES (?{tl}) {{ {ty} }}
            ?{el} sbol:type ?{tl} .
            """.format(ty=self.serialize_options(types), el=entity_label, tl=type_label)

    # Constructs a partial SPARQL query for all collection members with
    # at least one of the specified roles.
    def construct_role_pattern(self, roles, entity_label='entity', role_label='role'):
        if len(roles) == 0:
            return ""
        elif len(roles) == 1:
            return "?{el} sbol:role {ro} .".format(ro=self.serialize_objects(roles), el=entity_label)
        else:
            return """
            VALUES (?{rl}) {{ {ro} }}
            ?{el} sbol:role ?{rl} .
            """.format(ro=self.serialize_options(roles), el=entity_label, rl=role_label)

    def construct_custom_pattern(self, custom_properties, entity_label='entity'):
        query_arr = ['?{el} {qn} {obj} .'.format(el=entity_label, qn=qname, obj=custom_properties[qname]) if custom_properties[qname].startswith('<') and custom_properties[qname].endswith('>')
            else '?{el} {qn} "{obj}" .'.format(el=entity_label, qn=qname, obj=custom_properties[qname]) for qname in custom_properties]

        return '\n'.join(query_arr)

    def construct_definition_pattern(self, definitions, entity_label='entity', sub_entity_label='sub_entity'):
        if len(definitions) == 0:
            return ""
        elif len(definitions) == 1:
            return "?{el} sbol:definition {sd} .".format(el=entity_label, sd=self.serialize_objects(definitions))
        else:
            return """
            VALUES (?{sel}) {{ {df} }}
            ?{el} sbol:definition ?{sel} .
            """.format(el=entity_label, sel=sub_entity_label, df=self.serialize_options(definitions))

    def construct_sub_pattern(self, sub_entity_pattern="", definitions=[], entity_label='entity', sub_label='sub', sub_entity_label='sub_entity', rdf_type=None):
        if rdf_type is None:
            sub_predicate = "(sbol:component) (sbol:functionalComponent) (sbol:module)"
        elif rdf_type == 'http://sbols.org/v2#ComponentDefinition':
            sub_predicate = "(sbol:component)"
        elif rdf_type == 'http://sbols.org/v2#ModuleDefinition':
            sub_predicate = "(sbol:functionalComponent) (sbol:module)"

        if len(definitions) > 0:
            definition_pattern = self.construct_definition_pattern(definitions, sub_label, sub_entity_label)

            return """
            VALUES (?contains) {{ {sp} }}
            ?{el} ?contains ?{sl} .
            {dp}
            """.format(el=entity_label, sl=sub_label, dp=definition_pattern, sp=sub_predicate)
        elif len(sub_entity_pattern) > 0:
            return """
            VALUES (?contains) {{ {sp} }}
            ?{el} ?contains ?{sl} .
            ?{sl} sbol:definition ?{sel} .
            {sep}
            """.format(el=entity_label, sl=sub_label, sel=sub_entity_label, sep=sub_entity_pattern, sp=sub_predicate)
        else:
            return ""

    def construct_name_pattern(self, entity_label='entity', is_optional=True):
        if is_optional:
            return """
            OPTIONAL {{
                ?{el} dcterms:title ?name .
            }}
            """.format(el=entity_label)
        else:
            return """
            ?{el} dcterms:title ?name .
            """.format(el=entity_label)

    def construct_description_pattern(self, entity_label='entity', is_optional=True):
        if is_optional:
            return """
            OPTIONAL {{
                ?{el} dcterms:description ?description .
            }}
            """.format(el=entity_label)
        else:
            return """
            ?{el} dcterms:description ?description .
            """.format(el=entity_label)

    def construct_sequence_pattern(self, entity_label='entity'):
        # if is_optional:
        #     return """
        #     OPTIONAL {{
        #         ?{el} sbol:sequence ?seq .
        #         ?seq sbol:elements ?sequence .
        #     }}
        #     """.format(el=entity_label)
        # else:
        return """
        ?{el} sbol:sequence ?seq .
        ?seq sbol:elements ?sequence .
        """.format(el=entity_label)

    def construct_feature_pattern(self, entity_label='entity', sub_label='sub',
                                  sub_entity_label='feature'):
        return """
        ?{el} sbol:sequenceAnnotation ?seqAnno ;
            sbol:component ?{sl} .
        ?seqAnno sbol:component ?{sl} ;
            sbol:location ?location .
        ?location sbol:start ?start ;
            sbol:end ?end .
        ?{sl} sbol:definition ?{sel}
        """.format(el=entity_label, sl=sub_label, sel=sub_entity_label)

    def construct_rdf_type_pattern(self, rdf_type, entity_label='entity'):
        return """
        ?{el} rdf:type <{rt}> .
        """.format(el=entity_label, rt=rdf_type)

    def construct_entity_pattern(self, types=[], roles=[], all_types=True, sub_entity_pattern="", definitions=[], entity_label='entity', other_entity_labels=[], type_label='type', role_label='role', sub_label='sub', sub_entity_label='sub_entity', rdf_type=None, custom_properties=[]):
        if len(types) > 0 or len(roles) > 0 or len(sub_entity_pattern) > 0 or len(definitions) > 0 or rdf_type is not None:
            type_pattern = self.construct_type_pattern(types, all_types, entity_label, type_label)

            role_pattern = self.construct_role_pattern(roles, entity_label, role_label)

            sub_pattern = self.construct_sub_pattern(sub_entity_pattern, definitions, entity_label, sub_label, sub_entity_label)

            if rdf_type is not None:
                rdf_type_pattern = self.construct_rdf_type_pattern(rdf_type, entity_label)
            else:
                rdf_type_pattern = ""

            if 'name' in other_entity_labels:
                name_pattern = self.construct_name_pattern(entity_label)
            else:
                name_pattern = ""

            if 'description' in other_entity_labels:
                description_pattern = self.construct_description_pattern(entity_label)
            else:
                description_pattern = ""

            if 'sequence' in other_entity_labels:
                sequence_pattern = self.construct_sequence_pattern(entity_label)
            else:
                sequence_pattern = ""

            if 'feature' in other_entity_labels:
                feature_pattern = self.construct_feature_pattern(entity_label,
                                                                 sub_label)
            else:
                feature_pattern = ""

            if len(custom_properties) > 0:
                custom_pattern = self.construct_custom_pattern(custom_properties, entity_label)
            else:
                custom_pattern = ""

            return """
            {tp}
            {rp}
            {sp}
            {rt}
            {np}
            {dp}
            {qp}
            {fp}
            {cp}
            """.format(tp=type_pattern, rp=role_pattern, sp=sub_pattern, rt=rdf_type_pattern, np=name_pattern, dp=description_pattern, qp=sequence_pattern, fp=feature_pattern, cp=custom_pattern)
        else:
            return ""

    def construct_collection_pattern(self, collections=[], member_label='entity', members=[], member_cardinality='*', entity_label='entity', collection_label='collection'):
        member_pattern_switcher = {
            'exp': self.construct_experiment_pattern
        }

        try:
            construct_member_pattern = member_pattern_switcher[member_label]

            member_pattern = construct_member_pattern(members, entity_label, member_cardinality)
        except:
            member_pattern = ""

        if len(collections) > 0:
            if len(members) > 0:
                return """
                VALUES (?{cl}) {{ {col} }}
                VALUES (?{ml}) {{ {mem} }}
                ?{cl} sbol:member ?{ml} .
                {mp}
                """.format(col=self.serialize_options(collections), cl=collection_label, mem=self.serialize_options(members), ml=member_label, mp=member_pattern)
            else:
                return """
                VALUES (?{cl}) {{ {col} }}
                ?{cl} sbol:member ?{ml} .
                {mp}
                """.format(col=self.serialize_options(collections), cl=collection_label, ml=member_label, mp=member_pattern)
        else:
            if len(members) > 0:
                return """
                VALUES (?{ml}) {{ {mem} }}
                ?{cl} sbol:member ?{ml} .
                {mp}
                """.format(cl=collection_label, mem=self.serialize_options(members), ml=member_label, mp=member_pattern)
            else:
                return """
                ?{cl} sbol:member ?{ml} .
                {mp}
                """.format(cl=collection_label, ml=member_label, mp=member_pattern)

    def construct_experiment_pattern(self, experiments=[], entity_label='entity', sample_cardinality='*'):
        if len(sample_cardinality) > 0:
            derivation_path = 'prov:wasDerivedFrom{sc}/sbol:built'.format(sc=sample_cardinality)
        else:
            derivation_path = 'sbol:built'

        if len(experiments) == 0:
            return """
            ?exp sd2:experimentalData ?data .
            ?data prov:wasDerivedFrom ?sample .
            ?sample {dp} ?{el} .
            """.format(el=entity_label, dp=derivation_path)
        elif len(experiments) == 1:
            return """
            {exp} sd2:experimentalData ?data .
            ?data prov:wasDerivedFrom ?sample .
            ?sample {dp} ?{el} .
            """.format(exp=self.serialize_objects(experiments), el=entity_label, dp=derivation_path)
        else:
            return """
            VALUES (?exp) {{ {exp} }}
            ?exp sd2:experimentalData ?data .
            ?data prov:wasDerivedFrom ?sample .
            ?sample {dp} ?{el} .
            """.format(exp=self.serialize_options(experiments), el=entity_label, dp=derivation_path)

    # Constructs a SPARQL query for all members of the specified collection with
    # at least one of the specified types (or all of the specified types) and
    # at least one of the specified roles.
    def construct_collection_entity_query(self, collections, member_label='entity', types=[], roles=[], all_types=True, sub_types=[], sub_roles=[], definitions=[], all_sub_types=True, entity_label=None, other_entity_labels=[], members=[], member_cardinality='+', rdf_type=None, entity_depth=1, custom_properties=[], sub_entity_label='sub_entity'):
        target_labels = []
        if len(collections) > 1 or len(collections) == 0:
            target_labels.append('collection')

        if entity_label is None:
            entity_label = member_label

        if len(other_entity_labels) > 0:
            target_labels.extend(other_entity_labels)
        target_labels.append(entity_label)

        sub_entity_pattern = self.construct_entity_pattern(types=sub_types, roles=sub_roles, all_types=all_sub_types, entity_label=sub_entity_label, type_label='sub_type', role_label='sub_role')
        entity_pattern_1 = self.construct_entity_pattern(types, roles, all_types, sub_entity_pattern, definitions, entity_label, other_entity_labels, sub_entity_label=sub_entity_label, rdf_type=rdf_type, custom_properties=custom_properties)
        collection_pattern_1 = self.construct_collection_pattern(collections, member_label, members, member_cardinality, entity_label)

        if entity_depth == 1:
            return """
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX sbol: <http://sbols.org/v2#>
            PREFIX sd2: <http://sd2e.org#>
            PREFIX prov: <http://www.w3.org/ns/prov#>
            PREFIX dcterms: <http://purl.org/dc/terms/>
            SELECT DISTINCT ?{tl} WHERE {{
                {cp1}
                {ep1}
            }}
            """.format(tl=' ?'.join(target_labels), cp1=collection_pattern_1, ep1=entity_pattern_1)
        elif entity_depth == 2:
            sub_sub_entity_pattern = self.construct_entity_pattern(types=sub_types, roles=sub_roles, all_types=all_sub_types, entity_label=sub_entity_label, type_label='sub_type', role_label='sub_role')
            sub_entity_pattern = self.construct_entity_pattern(types, roles, all_types, sub_sub_entity_pattern, definitions, entity_label, other_entity_labels, rdf_type=rdf_type, custom_properties=custom_properties)
            entity_pattern_2 = self.construct_entity_pattern(sub_entity_pattern=sub_entity_pattern, sub_label='sub_prime', sub_entity_label=entity_label)

            collection_pattern_2 = self.construct_collection_pattern(collections, member_label, members, member_cardinality)

            return """
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX sbol: <http://sbols.org/v2#>
            PREFIX sd2: <http://sd2e.org#>
            PREFIX prov: <http://www.w3.org/ns/prov#>
            PREFIX dcterms: <http://purl.org/dc/terms/>
            SELECT DISTINCT ?{tl} WHERE {{ {{
                {cp1}
                {ep1}
            }} UNION {{
                {cp2}
                {ep2}
            }} }}
            """.format(tl=' ?'.join(target_labels), cp1=collection_pattern_1, cp2=collection_pattern_2, ep1=entity_pattern_1, ep2=entity_pattern_2)
        else:
            return ""

    def construct_unit_query(self, unit_id=None, name=None, symbol=None):
        if unit_id is not None or name is not None or symbol is not None:
            unit_query_fragments = []

            if unit_id is not None:
                om_uri = '/'.join([SBOLConstants.OM_NS[:-1], unit_id])

                unit_query_fragments.append("""
                    VALUES (?uri) {{ {uri} }}
                    ?uri rdfs:label ?name ;
                        om:symbol ?symbol .
                    FILTER( lang(?name) = "en" )
                """.format(uri=self.serialize_options([om_uri])))

            if name is not None:
                unit_query_fragments.append("""
                    VALUES (?name) {{ {nam} }}
                    ?uri rdfs:label ?name ;
                        om:symbol ?symbol .
                    FILTER( lang(?name) = "en" || lang(?name) = "nl" )
                """.format(nam=self.serialize_literal_options([name])))

            if symbol is not None:
                unit_query_fragments.append("""
                    ?uri rdfs:label ?name ;
                        om:symbol "{sym}" .
                    FILTER( lang(?name) = "en" )
                """.format(sym=symbol))

                unit_query_fragments.append("""
                    ?uri rdfs:label ?name ;
                        om:alternativeSymbol "{sym}" .
                    FILTER( lang(?name) = "en" )
                """.format(sym=symbol))

            unit_query_body = """
            } UNION {
            """.join(unit_query_fragments)

            return """
            SELECT ?uri ?name ?symbol WHERE {{ {{
            {bod}
            }} }}
            """.format(bod=unit_query_body)
        else:
            return ""

    def __format_group_binding(self, binding, binding_keys):
        if len(binding_keys) > 1 or len(binding_keys) == 0:
            return self.__format_entity_binding(binding, binding_keys)
        else:
            return binding[binding_keys[0]]['value']

    def __format_entity_binding(self, binding, binding_keys):
        formatted = {}

        for binding_key in binding_keys:
            try:
                formatted[binding_key] = binding[binding_key]['value']
            except:
                pass

        return formatted

    def __format_group(self, formatted, binding, binding_keys, group_key):
        group_value = binding[group_key]['value']

        if group_value in formatted:
            if not isinstance(formatted[group_value], list):
                formatted[group_value] = [formatted[group_value]]

            formatted[group_value].append(self.__format_group_binding(binding, binding_keys))
        else:
            formatted[group_value] = self.__format_group_binding(binding, binding_keys)

    def __format_entity(self, formatted, binding, binding_keys, entity_key):
        entity_value = binding[entity_key]['value']

        if entity_value in formatted:
            formatted_binding = self.__format_entity_binding(binding,
                                                            binding_keys)

            for key in formatted_binding.keys():
                if formatted[entity_value][key] != formatted_binding[key]:
                    if not isinstance(formatted[entity_value][key], list):
                        formatted[entity_value][key] = [formatted[entity_value][key]]

                    formatted[entity_value][key].append(formatted_binding[key])
        else:
            formatted[entity_value] = self.__format_entity_binding(binding, binding_keys)

    def format_query_result(self, query_result, binding_keys, group_key=None,
                            sort_key=None, entity_key=None, sub_binding_keys=[],
                            sub_group_key=None):
        if group_key is None and entity_key is None or len(binding_keys) == 0 and sub_group_key is None:
            if len(binding_keys) == 0:
                if group_key is not None:
                    binding_keys.append(group_key)
                elif entity_key is not None:
                    binding_keys.append(entity_key)

            formatted = []

            for binding in query_result['results']['bindings']:
                formatted.append(self.__format_group_binding(binding, binding_keys))
        else:
            formatted = {}

            if group_key is not None:
                for binding in query_result['results']['bindings']:
                    self.__format_group(formatted, binding, binding_keys, group_key)
            elif len(binding_keys) < 2 and sub_group_key is None:
                for binding in query_result['results']['bindings']:
                    self.__format_group(formatted, binding, binding_keys, entity_key)
            else:
                for binding in query_result['results']['bindings']:
                    self.__format_entity(formatted, binding, binding_keys, entity_key)

                if sub_group_key is not None:
                    for binding in query_result['results']['bindings']:
                        entity_value = binding[entity_key]['value']

                        if sub_group_key not in formatted[entity_value]:
                            formatted[entity_value][sub_group_key] = {}

                        self.__format_group(formatted[entity_value][sub_group_key], binding, sub_binding_keys, sub_group_key)

        if sort_key is not None:
            self.sort_query_result(formatted, sort_key)

        return formatted

    def sort_query_result(self, query_result, sort_key=None):
        if isinstance(query_result, list):
            self.__sort_query_list(query_result, sort_key)
        else:
            try:
                self.__sort_query_list(query_result['results']['bindings'],
                                       sort_key)
            except:
                for binding in query_result:
                    if isinstance(binding, list):
                        self.__sort_query_list(binding, sort_key)

    def __sort_query_list(self, query_list, sort_key=None):
        if sort_key is None:
            query_list.sort()
        else:
            try:
                query_list.sort(key=lambda x: x[sort_key]['value'])
            except:
                try:
                    query_list.sort(key=lambda x: x[sort_key])
                except:
                    query_list.sort()

    def query_experiment_components(self, types=[], collections=[], comp_label='comp', other_comp_labels=[], trace_derivation=True, roles=[], all_types=True, sub_types=[], sub_roles=[], definitions=[], all_sub_types=True, experiments=[], custom_properties=[]):
        if trace_derivation:
            sample_cardinality = '*'
        else:
            sample_cardinality = ''

        comp_query = self.construct_collection_entity_query(collections, 'exp', types, roles, all_types, sub_types, sub_roles, definitions, all_sub_types, comp_label, other_comp_labels, experiments, sample_cardinality, "http://sbols.org/v2#ComponentDefinition", 2, custom_properties)

        return self.fetch_SPARQL(self._server, comp_query)

    def query_experiment_modules(self, roles=[], collections=[], mod_label='mod', other_mod_labels=[], trace_derivation=True, sub_types=[], sub_roles=[], definitions=[], all_sub_types=True, experiments=[], custom_properties=[]):
        if trace_derivation:
            sample_cardinality = '*'
        else:
            sample_cardinality = ''

        mod_query = self.construct_collection_entity_query(collections, 'exp', roles=roles, sub_types=sub_types, sub_roles=sub_roles, definitions=definitions, all_sub_types=all_sub_types, entity_label=mod_label, other_entity_labels=other_mod_labels, members=experiments,
            member_cardinality=sample_cardinality, rdf_type="http://sbols.org/v2#ModuleDefinition", entity_depth=2, custom_properties=custom_properties)

        return self.fetch_SPARQL(self._server, mod_query)

    # Retrieves from the specified collection of design elements the URIs for all ComponentDefinitions with
    # at least one of the specified types (or all of the specified types) and at least one of the specified roles
    # This collection is typically associated with a challenge problem.
    def query_design_components(self, types=[], collections=[], comp_label='comp', other_comp_labels=[], roles=[], all_types=True, sub_types=[], sub_roles=[], definitions=[], all_sub_types=True, custom_properties=[], members=[]):
        comp_query = self.construct_collection_entity_query(collections, comp_label, types, roles, all_types, sub_types, sub_roles, definitions, all_sub_types, other_entity_labels=other_comp_labels, members=members, rdf_type="http://sbols.org/v2#ComponentDefinition", custom_properties=custom_properties)

        return self.fetch_SPARQL(self._server, comp_query)

    # Retrieves from the specified collection of design elements the URIs for all ModuleDefinitions with
    # at least one of the specified roles and that contain a FunctionalComponent or Module with
    # at least one of the specified sub-types (or all of the specified sub-types) and with
    # at least one of the specified roles.
    # This collection is typically associated with a challenge problem.
    def query_design_modules(self, roles=[], collections=[], mod_label='mod', other_mod_labels=[], sub_types=[], sub_roles=[], definitions=[], all_sub_types=True, custom_properties=[], sub_comp_label='sub_comp', members=[]):
        mod_query = self.construct_collection_entity_query(collections, mod_label, roles=roles, sub_types=sub_types, sub_roles=sub_roles, definitions=definitions, all_sub_types=all_sub_types, other_entity_labels=other_mod_labels, members=members, rdf_type="http://sbols.org/v2#ModuleDefinition", custom_properties=custom_properties, sub_entity_label=sub_comp_label)

        return self.fetch_SPARQL(self._server, mod_query)

    def query_collection_members(self, collections=[], members=[], rdf_type=None):
        mem_query = self.construct_collection_entity_query(collections, members=members, rdf_type=rdf_type)

        return self.fetch_SPARQL(self._server, mem_query)

    def query_collections(self, collections=[]):
        collection_query = self.construct_collection_entity_query(collections, entity_label='collection')

        return self.fetch_SPARQL(self._server, collection_query)

    def query_units(self, unit_id=None, name=None, symbol=None):
        unit_uris = []

        unit_query = self.construct_unit_query(unit_id, name, symbol)

        if self.om is not None:
            for unit_query_result in self.om.query(unit_query):
                unit_uris.append(unit_query_result.uri)

        return unit_uris

    def serialize_options(self, options):
        serial_options = []
        for opt in options:
            serial_options.append(''.join(['( <', opt, '> ) ']))

        return ''.join(serial_options)[:-1]

    def serialize_literal_options(self, options):
        serial_options = []
        for opt in options:
            serial_options.append(''.join(['( "', opt, '" ) ']))

        return ''.join(serial_options)[:-1]

    def serialize_objects(self, objects):
        serial_objects = []
        for obj in objects:
            serial_objects.append(''.join(['<', obj, '>, ']))

        return ''.join(serial_objects)[:-2]


def loadSBOLFile(sbolFile):
    sbolDoc = Document()
    sbolDoc.read(sbolFile)
    return sbolDoc


def login_SBH(server):
    sbh_connector = PartShop(server)
    sbh_user = input('Enter SynBioHub Username: ')
    sbh_connector.login(sbh_user, getpass.getpass(prompt='Enter SynBioHub Password: ', stream=sys.stderr))
    return sbh_connector


def export_definitions_to_csv(server, collections, csv_path):
    sbol_query = SBOLQuery(server)

    comps = sbol_query.format_query_result(sbol_query.query_design_components(collections=collections, other_comp_labels=['name']), ['comp', 'name'])

    mods = sbol_query.format_query_result(sbol_query.query_design_modules(collections=collections, other_mod_labels=['name']), ['mod', 'name'])

    with open(csv_path, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        for comp in comps:
            if 'name' in comp:
                csv_writer.writerow([comp['comp'], comp['name']])
            else:
                csv_writer.writerow([comp['comp'], ''])

        for mod in mods:
            if 'name' in mod:
                csv_writer.writerow([mod['mod'], mod['name']])
            else:
                csv_writer.writerow([mod['mod'], ''])
