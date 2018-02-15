from fetch_SPARQL import fetch_SPARQL


''' This module is used to query information from SD2's SynBioHub instance for DARPA's SD2E project.
	
	author(s) : Nicholas Roehner 
				Tramy Nguyen
''' 
class query_synbiohub():
	''' This class is used to connect to SD2's SynBioHub instance. 
		An instance of this class will allow a user to push and pull information from SynBioHub
		Each method stored in this class are SPARQL queries used to call to SynBioHub's instance.
	'''

	# server: The SynBioHub server to call sparql queries on.
	def __init__(self, server):
		self.__server = server

	# Retrieves all small molecule inducers from specified collection
	# collection: A collection aggregates all objects associated with a challenge problem or experiment plan
	def query_Inducer(self, collection):
		inducer_query = """
		PREFIX sbol: <http://sbols.org/v2#> 
		SELECT ?inducer WHERE {{
  			{col} sbol:member ?inducer .
  			?inducer sbol:type ?type;
           	sbol:role ?role .
  			FILTER ( ?type = <http://www.biopax.org/release/biopax-level3.owl#SmallMolecule> && ?role = <http://identifiers.org/chebi/CHEBI:35224> )
		}}""".format(col=collection)

		inducer_metadata = fetch_SPARQL(self.__server, inducer_query)
		return inducer_metadata

	# Retrieves all circular DNA from specified collection
	# collection: A collection aggregates all objects associated with a challenge problem or experiment plan
	# (Double braces get converted to single braces, since we're using format)
	def query_Plasmid(self, collection):
		plasmid_query = """
		PREFIX sbol: <http://sbols.org/v2#> 
		SELECT ?plasmid WHERE {{ 
  			{col} sbol:member ?plasmid .
  			?plasmid sbol:type ?type1, ?type2 .
  		FILTER ( ?type1 = <http://www.biopax.org/release/biopax-level3.owl#DnaRegion> && ?type2 = <http://identifiers.org/so/SO:0000988> ) 
		}}
		""".format(col=collection)

		plasmid_metadata = fetch_SPARQL(self.__server, plasmid_query)
		return plasmid_metadata

	# Retrieves all samples and associated experimental conditions from specified collection
	# collection: A collection aggregates all objects associated with a challenge problem or experiment plan
	def query_Sample(self, collection):
		sample_query = """
		PREFIX sbol: <http://sbols.org/v2#>
		PREFIX sd2: <http://sd2e.org#>
		SELECT ?sample ?condition WHERE {{
  			{col} sbol:member ?sample ;
        		sbol:member ?condition .
  			?sample sd2:built ?condition
		}}""".format(col=collection)

		sample_metadata = fetch_SPARQL(self.__server, sample_query)
		return sample_metadata