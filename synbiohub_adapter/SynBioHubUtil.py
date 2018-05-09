import getpass
import sys

from .fetch_SPARQL import fetch_SPARQL as _fetch_SPARQL
from sbol import *
from .cache_query import wrap_query_fn

'''
	This is a utility module containing classes with constant variables used for querying SynBioHub information
	
	author(s) : Nicholas Roehner 
				Tramy Nguyen
'''
class SBOLConstants():
	EFFECTOR = "http://identifiers.org/chebi/CHEBI:35224"
	FLUORESCEIN = "http://identifiers.org/chebi/CHEBI:31624"
	FLUORESCENCE = "http://purl.obolibrary.org/obo/NCIT_C16586"
	H2O = "http://identifiers.org/chebi/CHEBI:15377"

	LOGIC_OPERATOR = "http://edamontology.org/data_2133"

	BEAD = "http://purl.obolibrary.org/obo/NCIT_C70671"
	CONTROL = "http://purl.obolibrary.org/obo/NCIT_C28143"
	NCIT_STRAIN = "http://purl.obolibrary.org/obo/NCIT_C14419"
	
	MEDIA = "http://purl.obolibrary.org/obo/OBI_0000079"
	OBI_STRAIN = "http://purl.obolibrary.org/obo/OBI_0001185"

	SBOL_NS = "http://sbols.org/v2#"
	BBN_HOMESPACE = "https://synbiohub.bbn.com"

class BBNConstants():
	BBN_SERVER = "https://synbiohub.bbn.com/"
	BBN_YEASTGATES_COLLECTION = "https://synbiohub.bbn.com/user/tramyn/BBN_YEAST_GATES/BBN_YEAST_GATES_collection/1"
	BBN_RULE30_COLLECTION = 'https://synbiohub.bbn.com/user/tramyn/transcriptic_rule_30_q0_1_09242017/transcriptic_rule_30_q0_1_09242017_collection/1'

class SD2Constants():
	SD2_SERVER = "http://hub-api.sd2e.org:80/sparql"
	
	SD2_DESIGN_COLLECTION = 'https://hub.sd2e.org/user/sd2e/design/design_collection/1'
	RULE_30_DESIGN_COLLECTION = 'https://hub.sd2e.org/user/sd2e/design/rule_30/1'
	YEAST_GATES_DESIGN_COLLECTION = 'https://hub.sd2e.org/user/sd2e/design/yeast_gates/1'

	SD2_EXPERIMENT_COLLECTION = 'https://hub.sd2e.org/user/sd2e/experiment/experiment_collection/1'
	RULE_30_EXPERIMENT_COLLECTION = 'https://hub.sd2e.org/user/sd2e/experiment/rule_30/1'
	YEAST_GATES_EXPERIMENT_COLLECTION = 'https://hub.sd2e.org/user/sd2e/experiment/yeast_gates/1'
	
	LUDOX = 'https://hub.sd2e.org/user/sd2e/design/ludox_S40/1'

class SBHConstants():
	SD2_SERVER = "http://hub-api.sd2e.org:80/sparql"
	BBN_SERVER = "https://synbiohub.bbn.com/"
	BBN_YEASTGATES_COLLECTION = "https://synbiohub.bbn.com/user/tramyn/BBN_YEAST_GATES/BBN_YEAST_GATES_collection/1"
	BBN_RULE30_COLLECTION = 'https://synbiohub.bbn.com/user/tramyn/transcriptic_rule_30_q0_1_09242017/transcriptic_rule_30_q0_1_09242017_collection/1'
	RULE_30_EXPERIMENT_COLLECTION = 'https://hub.sd2e.org/user/sd2e/experiment/rule_30/1'
	YEAST_GATES_EXPERIMENT_COLLECTION = 'https://hub.sd2e.org/user/sd2e/experiment/yeast_gates/1'
	RULE_30_DESIGN_COLLECTION = 'https://hub.sd2e.org/user/sd2e/design/rule_30/1'
	YEAST_GATES_DESIGN_COLLECTION = 'https://hub.sd2e.org/user/sd2e/design/yeast_gates/1'
	SD2_DESIGN_COLLECTION = 'https://hub.sd2e.org/user/sd2e/design/design_collection/1'
	SD2_EXPERIMENT_COLLECTION = 'https://hub.sd2e.org/user/sd2e/experiment/experiment_collection/1'

class SBOLQuery():
	''' This class structures SPARQL queries for objects belonging to classes from the SBOL data model. 
		An instance of this class will allow a user to pull information on these objects from the specified instance of SynBioHub.
	'''

	# server: The SynBioHub server to call sparql queries on.
	def __init__(self, server, use_fallback_cache=False):
		self._server = server
		self._use_fallback_cache = use_fallback_cache

		# If using fallback cache, wrap the fetch_SPARQL function
		# with cache storage/retrieval.
		if use_fallback_cache:
			self.fetch_SPARQL = wrap_query_fn(_fetch_SPARQL)
		else:
			self.fetch_SPARQL = _fetch_SPARQL

	# Constructs a partial SPARQL query for all collection members with 
	# at least one of the specified types (or all of the specified types). 
	def construct_type_pattern(self, types, all_types=True, entity_label='entity', type_label='type'):
		if len(types) > 0:
			if all_types or len(types) == 1:
				return "?{el} sbol:type {ty} .".format(ty=self.serialize_objects(types), el=entity_label)
			else:
				return """
				VALUES (?{tl}) {{ {ty} }}
				?{el} sbol:type ?{tl} .
				""".format(ty=self.serialize_options(types), el=entity_label, tl=type_label)
		else:
			return ""

	# Constructs a partial SPARQL query for all collection members with 
	# at least one of the specified roles. 
	def construct_role_pattern(self, roles, entity_label='entity', role_label='role'):
		if len(roles) > 0:
			if len(roles) > 1:
				return """
				VALUES (?{rl}) {{ {ro} }}
				?{el} sbol:role ?{rl} .
				""".format(ro=self.serialize_options(roles), el=entity_label, rl=role_label)
			else:
				return "?{el} sbol:role {ro} .".format(ro=self.serialize_objects(roles), el=entity_label)
		else:
			return ""

	def construct_definition_pattern(self, definitions, sub_label='sub', sub_entity_label='sub_entity'):
		if len(definitions) > 0:
			if len(definitions) > 1:
				return """
				VALUES (?{sel}) {{ {sd} }}
				?{sl} sbol:definition ?{sel} .
				""".format(sl=sub_label, sel=sub_entity_label, sd=self.serialize_options(definitions))
			else:
				return "?{sl} sbol:definition {sd} .".format(sl=sub_label, sd=self.serialize_objects(definitions))
		else:
			return ""

	def construct_sub_pattern(self, sub_entity_pattern="", definitions=[], entity_label='entity', sub_label='sub', sub_entity_label='sub_entity'):
		if len(definitions) > 0:
			definition_pattern = self.construct_definition_pattern(definitions, sub_label, sub_entity_label)

			return """
			VALUES (?contains) {{ (sbol:component) (sbol:functionalComponent) (sbol:module) }}
			?{el} ?contains ?{sl} .
			{dp}
			""".format(el=entity_label, sl=sub_label, dp=definition_pattern)
		elif len(sub_entity_pattern) > 0:
			return """
			VALUES (?contains) {{ (sbol:component) (sbol:functionalComponent) (sbol:module) }}
			?{el} ?contains ?{sl} .
			?{sl} sbol:definition ?{sel} .
			{sep}
			""".format(el=entity_label, sl=sub_label, sel=sub_entity_label, sep=sub_entity_pattern)
		else:
			return ""

	def construct_entity_pattern(self, types=[], roles=[], all_types=True, sub_entity_pattern="", definitions=[], entity_label='entity', type_label='type', role_label='role', sub_label='sub', sub_entity_label='sub_entity'):
		if len(types) > 0 or len(roles) > 0 or len(sub_entity_pattern) > 0 or len(definitions) > 0:
			type_pattern = self.construct_type_pattern(types, all_types, entity_label, type_label)

			role_pattern = self.construct_role_pattern(roles, entity_label, role_label)

			sub_pattern = self.construct_sub_pattern(sub_entity_pattern, definitions, entity_label, sub_label, sub_entity_label)

			return """
			{tp}
			{rp}
			{sp}
			""".format(tp=type_pattern, rp=role_pattern, sp=sub_pattern)
		else:
			return ""

	def construct_member_entity_pattern(self, collection, entity_pattern, member_label='entity', member_pattern="", member=None):
		if member is None:
			member_obj = '?' + member_label
		else:
			member_obj = ''.join(['<', member, '>'])

		return """ 
		<{col}> sbol:member {mo} .
		{mp}
		{ep}
		""".format(col=collection, mo=member_obj, mp=member_pattern, ep=entity_pattern)

	def construct_experiment_pattern(self, experiment=None, entity_label='entity'):
		if experiment is None:
			return """
			?exp sd2:experimentalData ?data .
			?data prov:wasDerivedFrom ?sample .
			?sample sbol:built ?{el} .
			""".format(el=entity_label)
		else:
			return """
			<{exp}> sd2:experimentalData ?data .
			?data prov:wasDerivedFrom ?sample .
			?sample sbol:built ?{el} .
			""".format(exp=experiment, el=entity_label)

	# Constructs a SPARQL query for all members of the specified collection with
	# at least one of the specified types (or all of the specified types) and
	# at least one of the specified roles.
	def construct_collection_entity_query(self, collection, member_label='entity', types=[], roles=[], all_types=True, sub_types=[], sub_roles=[], definitions=[], all_sub_types=True, entity_label=None, member=None):
		if entity_label is None:
			entity_label = member_label

		pattern_switcher = {
			'exp': self.construct_experiment_pattern
		}

		try:
			construct_pattern = pattern_switcher[member_label]

			member_pattern_1 = construct_pattern(member, entity_label)
			member_pattern_2 = construct_pattern(member)
		except:
			member_pattern_1 = ""
			member_pattern_2 = ""

		sub_entity_pattern = self.construct_entity_pattern(types=sub_types, roles=sub_roles, all_types=all_sub_types, entity_label='sub_entity', type_label='sub_type', role_label='sub_role')
		entity_pattern = self.construct_entity_pattern(types, roles, all_types, sub_entity_pattern, definitions, entity_label)

		member_entity_pattern_1 = self.construct_member_entity_pattern(collection, entity_pattern, member_label, member_pattern_1, member)

		sub_sub_entity_pattern = self.construct_entity_pattern(types=sub_types, roles=sub_roles, all_types=all_sub_types, entity_label='sub_entity', type_label='sub_type', role_label='sub_role')
		sub_entity_pattern = self.construct_entity_pattern(types, roles, all_types, sub_sub_entity_pattern, definitions, entity_label)
		entity_pattern = self.construct_entity_pattern(sub_entity_pattern=sub_entity_pattern, sub_label='sub_prime', sub_entity_label=entity_label)

		if member_label == entity_label:
			member_label = 'entity'

		member_entity_pattern_2 = self.construct_member_entity_pattern(collection, entity_pattern, member_label, member_pattern_2, member)

		return """
		PREFIX sbol: <http://sbols.org/v2#>
		PREFIX sd2: <http://sd2e.org#>
		PREFIX prov: <http://www.w3.org/ns/prov#>
		SELECT DISTINCT ?{el} WHERE {{ {{
			{mep1}
		}} UNION {{
			{mep2}
		}} }}
		""".format(el=entity_label, mep1=member_entity_pattern_1, mep2=member_entity_pattern_2)

	def query_experiment_set_components(self, types, collection=SD2Constants.SD2_EXPERIMENT_COLLECTION, comp_label='comp', roles=[], all_types=True, sub_types=[], sub_roles=[], definitions=[], all_sub_types=True, experiment=None):
		comp_query = self.construct_collection_entity_query(collection, 'exp', types, roles, all_types, sub_types, sub_roles, definitions, all_sub_types, comp_label, experiment)

		return self.fetch_SPARQL(self._server, comp_query)

	def query_experiment_set_modules(self, roles, collection=SD2Constants.SD2_EXPERIMENT_COLLECTION, mod_label='mod', sub_types=[], sub_roles=[], definitions=[], all_sub_types=True, experiment=None):
		mod_query = self.construct_collection_entity_query(collection=collection, member_label='exp', roles=roles, sub_types=sub_types, sub_roles=sub_roles, definitions=definitions, all_sub_types=all_sub_types, entity_label=mod_label, member=experiment)

		return self.fetch_SPARQL(self._server, mod_query)

	# Retrieves from the specified collection of design elements the URIs for all ComponentDefinitions with 
	# at least one of the specified types (or all of the specified types) and at least one of the specified roles 
	# This collection is typically associated with a challenge problem.
	def query_design_set_components(self, types, collection=SD2Constants.SD2_DESIGN_COLLECTION, comp_label='comp', roles=[], all_types=True, sub_types=[], sub_roles=[], definitions=[], all_sub_types=True):
		comp_query = self.construct_collection_entity_query(collection, comp_label, types, roles, all_types, sub_types, sub_roles, definitions, all_sub_types)

		return self.fetch_SPARQL(self._server, comp_query)

	# Retrieves from the specified collection of design elements the URIs for all ModuleDefinitions with 
	# at least one of the specified roles and that contain a FunctionalComponent or Module with 
	# at least one of the specified sub-types (or all of the specified sub-types) and with 
	# at least one of the specified roles.
	# This collection is typically associated with a challenge problem.
	def query_design_set_modules(self, roles, collection=SD2Constants.SD2_DESIGN_COLLECTION, mod_label='mod', sub_types=[], sub_roles=[], definitions=[], all_sub_types=True):
		mod_query = self.construct_collection_entity_query(collection=collection, member_label=mod_label, roles=roles, sub_types=sub_types, sub_roles=sub_roles, definitions=definitions, all_sub_types=all_sub_types)

		return self.fetch_SPARQL(self._server, mod_query)

	def serialize_options(self, options):
		serial_options = []
		for opt in options:
			serial_options.append(''.join(['( <', opt, '> ) ']))

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