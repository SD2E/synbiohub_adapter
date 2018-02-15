'''
	This is a utility module containing classes with constant variables used for querying SynBioHub information
	
	author(s) : Nicholas Roehner 
				Tramy Nguyen
'''
class SBOLConstants():
	CIRCULAR = "http://identifiers.org/so/SO:0000988"
	DNA_REGION = "http://www.biopax.org/release/biopax-level3.owl#DnaRegion"
	EFFECTOR = "http://identifiers.org/chebi/CHEBI:35224"
	SMALL_MOLECULE = "<http://www.biopax.org/release/biopax-level3.owl#SmallMolecule>"

	SBOL_NS = "http://sbols.org/v2#"

class SBHConstants():
	SD2_SERVER = "http://hub-api.sd2e.org:80/sparql"
	RULE30_COLLECTION = '<http://hub.sd2e.org/user/nicholasroehner/rule_30/rule_30_collection/1>'
