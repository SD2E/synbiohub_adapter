from fetch_SPARQL import fetch_SPARQL


''' 
	This module is used to query information from SD2's SynBioHub instance for DARPA's SD2E project.
	
	author(s) : Nicholas Roehner 
				Tramy Nguyen
''' 
class SynBioHubQuery():
	''' This class is used to connect to SD2's SynBioHub instance. 
		An instance of this class will allow a user to push and pull information from SynBioHub
		Each method stored in this class are SPARQL queries used to call to SynBioHub's instance.
	'''

	# server: The SynBioHub server to call sparql queries on.
	def __init__(self, server):
		self.__server = server

	# Retrieves the URIs for all inducers in the specified challenge problem
	def query_challenge_inducers(self, collection):
		inducer_query = """
		PREFIX sbol: <http://sbols.org/v2#>
		PREFIX sd2: <http://sd2e.org#>
		PREFIX prov: <http://www.w3.org/ns/prov#> 
		SELECT DISTINCT ?inducer WHERE {{ 
  			{col} sbol:member ?exp .
  			?exp sd2:experimentalData ?data .
  			?data prov:wasDerivedFrom ?sample .
  			?sample sd2:built ?condition .
  			?condition sbol:functionalComponent ?fc .
  			?fc sbol:definition ?inducer .
  			?inducer sbol:type ?type;
           		sbol:role ?role .
  		FILTER ( ?type = <http://www.biopax.org/release/biopax-level3.owl#SmallMolecule> && 
  			?role = <http://identifiers.org/chebi/CHEBI:35224> )
		}}
		""".format(col=collection)

		return fetch_SPARQL(self.__server, inducer_query)

	# Retrieves the URIs for all plasmids in the specified challenge problem
	def query_challenge_plasmids(self, collection):
		plasmid_query = """
		PREFIX sbol: <http://sbols.org/v2#>
		PREFIX sd2: <http://sd2e.org#>
		PREFIX prov: <http://www.w3.org/ns/prov#> 
		SELECT DISTINCT ?plasmid WHERE {{ 
  			{col} sbol:member ?exp .
  			?exp sd2:experimentalData ?data .
  			?data prov:wasDerivedFrom ?sample .
  			?sample sd2:built ?condition .
  			?condition sd2:plasmid ?plasmid
		}}
		""".format(col=collection)

		return fetch_SPARQL(self.__server, plasmid_query)

	# Retrieves the URIs for all inducers in the specified experiment
	def query_experiment_inducers(self, experiment):
		inducer_query = """
		PREFIX sbol: <http://sbols.org/v2#>
		PREFIX sd2: <http://sd2e.org#>
		PREFIX prov: <http://www.w3.org/ns/prov#> 
		SELECT DISTINCT ?inducer WHERE {{ 
  			{exp} sd2:experimentalData ?data .
  			?data prov:wasDerivedFrom ?sample .
  			?sample sd2:built ?condition .
  			?condition sbol:functionalComponent ?fc .
  			?fc sbol:definition ?inducer .
  			?inducer sbol:type ?type;
           		sbol:role ?role .
  		FILTER ( ?type = <http://www.biopax.org/release/biopax-level3.owl#SmallMolecule> && 
  			?role = <http://identifiers.org/chebi/CHEBI:35224> ) 
		}}
		""".format(exp=experiment)

		return fetch_SPARQL(self.__server, inducer_query)

	# Retrieves the URIs for all plasmids in the specified experiment
	def query_experiment_plasmids(self, experiment):
		plasmid_query = """
		PREFIX sd2: <http://sd2e.org#>
		PREFIX prov: <http://www.w3.org/ns/prov#> 
		SELECT DISTINCT ?plasmid WHERE {{ 
  			{exp} sd2:experimentalData ?data .
  			?data prov:wasDerivedFrom ?sample .
  			?sample sd2:built ?condition .
  			?condition sd2:plasmid ?plasmid
		}}
		""".format(exp=experiment)

		return fetch_SPARQL(self.__server, plasmid_query)

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