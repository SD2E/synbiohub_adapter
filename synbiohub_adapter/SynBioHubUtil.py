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
	def construct_type_pattern(self, types, all_types=True, entity_label='entity', type_label='type'):
		if all_types:
			return "?{el} sbol:type {ty}".format(ty=self.serialize_objects(types), el=entity_label)
		else:
			return """
			VALUES (?{tl}) {{ {ty} }}
			?{el} sbol:type ?{tl} .
			""".format(ty=self.serialize_options(types), el=entity_label, tl=type_label)

	# Constructs a partial SPARQL query for all collection members with 
	# at least one of the specified roles. 
	def construct_role_pattern(self, roles, entity_label='entity', role_label='role'):
		return """
		VALUES (?{rl}) {{ {ro} }}
		?{el} sbol:role ?{rl} .
		""".format(ro=self.serialize_options(roles), el=entity_label, rl=role_label)

	# Constructs a partial SPARQL query for all collection members that contain a Component
	# or a FunctionalComponent with at least one of the specified types 
	# (or all of the specified types)
	def construct_sub_type_pattern(self, types, all_types=True, entity_label='entity', sub_label='subDef'):
		type_pattern = self.construct_type_pattern(types, all_types, sub_label, 'subType')

		return """
		VALUES (?contains) {{ (sbol:component) (sbol:functionalComponent) }}
		?{el} ?contains ?sub .
		?sub sbol:definition ?{sl} .
		{ty}
		""".format(ty=type_pattern, el=entity_label, sl=sub_label)

	# Constructs a partial SPARQL query for all collection members that contain a Component,
	# FunctionalComponent, or Module with at least one of the specified roles. 
	def construct_sub_role_pattern(self, roles, entity_label='entity', sub_label='subDef'):
		role_pattern = self.construct_role_pattern(roles, sub_label, 'subRole')

		return """
		VALUES (?contains) {{ (sbol:component) (sbol:functionalComponent) (sbol:module) }}
		?{el} ?contains ?sub .
		?sub sbol:definition ?{sl} .
		{ro}
		""".format(ro=role_pattern, el=entity_label, sl=sub_label)

	# Constructs a partial SPARQL query for all collection members that contain a Component,
	# FunctionalComponent, or Module with at least one of the specified sub-definitions. 
	def construct_sub_definition_pattern(self, definitions, entity_label='entity', sub_label='subDef'):
		return """
		VALUES (?contains) {{ (sbol:component) (sbol:functionalComponent) (sbol:module) }}
		?{el} ?contains ?sub .
		VALUES (?{sl}) {{ {de} }}
		?sub sbol:definition ?{sl} .
		""".format(de=self.serialize_options(definitions), el=entity_label, sl=sub_label)

	def construct_experiment_pattern(self, experiment=None):
		if experiment is None:
			return """
			?exp sd2:experimentalData ?data .
			?data prov:wasDerivedFrom ?sample .
			?sample sbol:built ?condition .
			"""
		else:
			return """
			<{exp}> sd2:experimentalData ?data .
			?data prov:wasDerivedFrom ?sample .
			?sample sbol:built ?condition .
			""".format(exp=experiment)

	# Constructs a SPARQL query for all members of the specified collection with
	# at least one of the specified types (or all of the specified types) and
	# at least one of the specified roles.
	def construct_member_query(self, collection, member_label='mem', types=[], roles=[], all_types=True, sub_types=[], sub_roles=[], sub_definitions=[], all_sub_types=True, target_label=None, sub_target_label=None, member=None, member_pattern=""):
		if target_label is None:
			target_label = member_label

		if len(types) > 0:
			if sub_target_label is None:
				type_pattern = self.construct_type_pattern(types, all_types, target_label)
			else:
				type_pattern = self.construct_type_pattern(types, all_types, target_label, sub_target_label)
		else:
			type_pattern = ""

		if len(roles) > 0:
			if sub_target_label is None:
				role_pattern = self.construct_role_pattern(roles, target_label)
			else:
				role_pattern = self.construct_role_pattern(roles, target_label, sub_target_label)
		else:
			role_pattern = ""

		if len(sub_types) > 0:
			if sub_target_label is None:
				sub_type_pattern = self.construct_sub_type_pattern(sub_types, all_sub_types, target_label)
			else:
				sub_type_pattern = self.construct_sub_type_pattern(sub_types, all_sub_types, target_label, sub_target_label)
		else:
			sub_type_pattern = ""

		if len(sub_roles) > 0:
			if sub_target_label is None:
				sub_role_pattern = self.construct_sub_role_pattern(sub_roles, target_label)
			else:
				sub_role_pattern = self.construct_sub_role_pattern(sub_roles, target_label, sub_target_label)
		else:
			sub_role_pattern = ""

		if len(sub_definitions) > 0:
			if sub_target_label is None:
				sub_def_pattern = self.construct_sub_definition_pattern(sub_definitions, target_label)
			else:
				sub_def_pattern = self.construct_sub_definition_pattern(sub_definitions, target_label, sub_target_label)
		else:
			sub_def_pattern = ""

		if member is None:
			member_obj = '?' + member_label
		else:
			member_obj = ''.join(['<', member, '>'])

		if sub_target_label is None:
			return """
			PREFIX sbol: <http://sbols.org/v2#>
			PREFIX sd2: <http://sd2e.org#>
			PREFIX prov: <http://www.w3.org/ns/prov#>
			SELECT DISTINCT ?{tl} WHERE {{ 
				<{col}> sbol:member {mo} .
				{mp}
				{ty}
				{ro}
				{sty}
				{sro}
				{sde}
			}}
			""".format(tl=target_label, col=collection, mo=member_obj, mp=member_pattern, ty=type_pattern, ro=role_pattern, sty=sub_type_pattern, sro=sub_role_pattern, sde=sub_def_pattern)
		else:
			return """
			PREFIX sbol: <http://sbols.org/v2#>
			PREFIX sd2: <http://sd2e.org#>
			PREFIX prov: <http://www.w3.org/ns/prov#>
			SELECT DISTINCT ?{tl} WHERE {{ 
				<{col}> sbol:member {mo} .
				{mp}
				{ty}
				{ro}
				{sty}
				{sro}
				{sde}
			}}
			""".format(tl=sub_target_label, col=collection, mo=member_obj, mp=member_pattern, ty=type_pattern, ro=role_pattern, sty=sub_type_pattern, sro=sub_role_pattern, sde=sub_def_pattern)

	def query_experiment_set_components(self, types, collection=SD2Constants.SD2_EXPERIMENT_COLLECTION, comp_label='comp', roles=[], all_types=True, experiment=None):
		exp_pattern = self.construct_experiment_pattern(experiment)

		comp_query = self.construct_member_query(collection=collection, member_label='exp', sub_types=types, sub_roles=roles, all_sub_types=all_types, target_label='condition', sub_target_label=comp_label, member=experiment, member_pattern=exp_pattern)

		return self.fetch_SPARQL(self._server, comp_query)

	def query_experiment_set_modules(self, roles, collection=SD2Constants.SD2_EXPERIMENT_COLLECTION, mod_label='mod', experiment=None):
		exp_pattern = self.construct_experiment_pattern(experiment)

		mod_query = self.construct_member_query(collection=collection, member_label='exp', sub_roles=roles, target_label='condition', sub_target_label=mod_label, member=experiment, member_pattern=exp_pattern)

		return self.fetch_SPARQL(self._server, mod_query)

	# Retrieves from the specified collection of design elements the URIs for all ComponentDefinitions with 
	# at least one of the specified types (or all of the specified types) and at least one of the specified roles 
	# This collection is typically associated with a challenge problem.
	def query_design_set_components(self, types, collection=SD2Constants.SD2_DESIGN_COLLECTION, comp_label='comp', roles=[], all_types=True, sub_types=[], sub_roles=[], sub_definitions=[], all_sub_types=True):
		comp_query = self.construct_member_query(collection, comp_label, types, roles, all_types, sub_types, sub_roles, sub_definitions, all_sub_types)

		return self.fetch_SPARQL(self._server, comp_query)

	# Retrieves from the specified collection of design elements the URIs for all ModuleDefinitions with 
	# at least one of the specified roles and that contain a FunctionalComponent or Module with 
	# at least one of the specified sub-types (or all of the specified sub-types) and with 
	# at least one of the specified roles.
	# This collection is typically associated with a challenge problem.
	def query_design_set_modules(self, roles, collection=SD2Constants.SD2_DESIGN_COLLECTION, mod_label='mod', sub_types=[], sub_roles=[], sub_definitions=[], all_sub_types=True):
		mod_query = self.construct_member_query(collection=collection, member_label=mod_label, roles=roles, sub_types=sub_types, sub_roles=sub_roles, sub_definitions=sub_definitions, all_sub_types=all_sub_types)

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