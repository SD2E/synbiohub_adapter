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
	FLUORESCENT_PROBE = "http://identifiers.org/chebi/CHEBI:39442"
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
	def construct_member_type_query(self, types, all_types=True):
		if all_types:
			return "?mem sbol:type {ty}".format(ty=self.serialize_objects(types))
		else:
			return """
			VALUES (?type) {{ {ty} }}
			?mem sbol:type ?type .
			""".format(ty=self.serialize_options(types))

	# Constructs a partial SPARQL query for all collection members with 
	# at least one of the specified roles. 
	def construct_member_role_query(self, roles):
		return """
		VALUES (?role) {{ {ro} }}
		?mem sbol:role ?role .
		""".format(ro=self.serialize_options(roles))

	# Constructs a partial SPARQL query for all collection members that contain a Component
	# or a FunctionalComponent with at least one of the specified types 
	# (or all of the specified types)
	def construct_member_sub_type_query(self, types, all_types=True):
		return """
		VALUES (?contains) {{ (sbol:component) (sbol:functionalComponent) }}
		?mem ?contains ?sub .
		?sub sbol:definition ?def .
		VALUES (?subType) {{ {ty} }}
		?def sbol:type ?subType .
		""".format(ty=self.serialize_options(types))

	# Constructs a partial SPARQL query for all collection members that contain a Component,
	# FunctionalComponent, or Module with at least one of the specified roles. 
	def construct_member_sub_role_query(self, roles):
		return """
		VALUES (?contains) {{ (sbol:component) (sbol:functionalComponent) (sbol:module) }}
		?mem ?contains ?sub .
		?sub sbol:definition ?def .
		VALUES (?subRole) {{ {ro} }}
		?def sbol:role ?subRole .
		""".format(ro=self.serialize_options(roles))

	# Constructs a partial SPARQL query for all collection members that contain a Component,
	# FunctionalComponent, or Module with at least one of the specified sub-definitions. 
	def construct_member_sub_definition_query(self, definitions):
		return """
		VALUES (?contains) {{ (sbol:component) (sbol:functionalComponent) (sbol:module) }}
		?mem ?contains ?sub .
		VALUES (?def) {{ {de} }}
		?sub sbol:definition ?def .
		""".format(de=self.serialize_options(definitions))

	# Constructs a SPARQL query for all members of the specified collection with
	# at least one of the specified types (or all of the specified types) and
	# at least one of the specified roles.
	def construct_member_query(self, collection, types=[], roles=[], all_types=True, sub_types=[], sub_roles=[], sub_definitions=[], all_sub_types=True):
		if len(types) > 0:
			type_query = self.construct_member_type_query(types, all_types)
		else:
			type_query = ""

		if len(roles) > 0:
			role_query = self.construct_member_role_query(roles)
		else:
			role_query = ""

		if len(sub_types) > 0:
			sub_type_query = self.construct_member_sub_type_query(sub_types, all_sub_types)
		else:
			sub_type_query = ""

		if len(sub_roles) > 0:
			sub_role_query = self.construct_member_sub_role_query(sub_roles)
		else:
			sub_role_query = ""

		if len(sub_definitions) > 0:
			sub_definition_query = self.construct_member_sub_definition_query(sub_definitions)
		else:
			sub_definition_query = ""

		return """
		PREFIX sbol: <http://sbols.org/v2#>
		SELECT DISTINCT ?mem WHERE {{ 
			<{col}> sbol:member ?mem .
			{ty}
			{ro}
			{sty}
			{sro}
			{sde}
		}}
		""".format(col=collection, ty=type_query, ro=role_query, sty=sub_type_query, sro=sub_role_query, sde=sub_definition_query)
		
	# Retrieves from the specified collection of design elements the URIs for all ComponentDefinitions with 
	# at least one of the specified types (or all of the specified types) and at least one of the specified roles 
	# This collection is typically associated with a challenge problem.
	def query_design_set_components(self, collection, types, roles=[], all_types=True):
		comp_query = self.construct_member_query(collection, types, roles, all_types)

		return self.fetch_SPARQL(self._server, comp_query)

	# Retrieves from the specified collection of design elements the URIs for all ModuleDefinitions with 
	# at least one of the specified roles and that contain a FunctionalComponent or Module with 
	# at least one of the specified sub-types (or all of the specified sub-types) and with 
	# at least one of the specified roles.
	# This collection is typically associated with a challenge problem.
	def query_design_set_modules(self, collection, roles, sub_types=[], sub_roles=[], sub_definitions=[], all_sub_types=False):
		mod_query = self.construct_member_query(collection=collection, roles=roles, sub_types=sub_types, sub_roles=sub_roles, sub_definitions=sub_definitions, all_sub_types=all_sub_types)

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