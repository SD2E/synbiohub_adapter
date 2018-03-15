import getpass
import sys

from .fetch_SPARQL import fetch_SPARQL
from sbol import *

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

	# Retrieves the URIs for all logic gates in the specified collection of design elements
	# This collection is typically associated with a challenge problem
	def query_design_gates(self, collection):
		gate_query = """
		PREFIX sbol: <http://sbols.org/v2#>
		SELECT DISTINCT ?gate WHERE {{ 
  			{col} sbol:member ?gate .
  			?gate sbol:role ?role .
  		FILTER ( ?role = <http://edamontology.org/data_2133> )
		}}
		""".format(col=collection)

		return fetch_SPARQL(self.__server, gate_query)

	# Retrieves the URIs for all inducers in the specified collection of design elements
	# This collection is typically associated with a challenge problem
	def query_design_inducers(self, collection):
		inducer_query = """
		PREFIX sbol: <http://sbols.org/v2#>
		SELECT DISTINCT ?inducer WHERE {{ 
  			{col} sbol:member ?inducer .
  			?inducer sbol:type ?type;
           		sbol:role ?role .
  		FILTER ( ?type = <http://www.biopax.org/release/biopax-level3.owl#SmallMolecule> && 
  			?role = <http://identifiers.org/chebi/CHEBI:35224> )
		}}
		""".format(col=collection)

		return fetch_SPARQL(self.__server, inducer_query)

	# Retrieves the URIs for all plasmids in the specified collection of design elements
	# This collection is typically associated with a challenge problem
	def query_design_plasmids(self, collection):
		plasmid_query = """
		PREFIX sbol: <http://sbols.org/v2#>
		SELECT DISTINCT ?plasmid WHERE {{ 
  			{col} sbol:member ?plasmid .
  			?plasmid sbol:type ?type1;
           		sbol:type ?type2 .
  		FILTER ( ?type1 = <http://www.biopax.org/release/biopax-level3.owl#DnaRegion> && 
  			?type2 = <http://identifiers.org/so/SO:0000988> )
		}}
		""".format(col=collection)

		return fetch_SPARQL(self.__server, plasmid_query)

	# Retrieves the URIs for all strains in the specified collection of design elements
	# This collection is typically associated with a challenge problem
	def query_design_strains(self, collection):
		strain_query = """
		PREFIX sbol: <http://sbols.org/v2#>
		SELECT DISTINCT ?strain WHERE {{ 
  			{col} sbol:member ?strain .
  			?strain sbol:type ?type .
  		FILTER ( ?type = <http://purl.obolibrary.org/obo/NCIT_C14419> || 
  			?type = <http://purl.obolibrary.org/obo/OBI_0001185> )
		}}
		""".format(col=collection)

		return fetch_SPARQL(self.__server, strain_query)

	# Retrieves the URIs for all collections of experiments
	# These collections are typically associated with challenge problems
	def query_experiment_sets(self):
		challenge_query = """
		PREFIX sbol: <http://sbols.org/v2#>
		PREFIX sd2: <http://sd2e.org#>
		SELECT DISTINCT ?collection WHERE {{ 
  			?collection sbol:member ?exp .
  			?exp sd2:experimentalData ?data .
  			FILTER NOT EXISTS {{
  				?collection sbol:member ?m .
  				FILTER ( ?m != ?exp )
  			}}
		}}
		"""

		return fetch_SPARQL(self.__server, challenge_query)

	# Retrieves the size of the specificed collection of experiments
	# This collection is typically associated with a challenge problem
	def query_experiment_set_count(self, collection):
		experiment_count_query = """
		PREFIX sbol: <http://sbols.org/v2#>
		PREFIX sd2: <http://sd2e.org#>
		SELECT (count(distinct ?exp) as ?expcount) WHERE {{ 
  			{col} sbol:member ?exp .
  			?exp sd2:experimentalData ?data
		}}
		""".format(col=collection)

		return fetch_SPARQL(self.__server, experiment_count_query)

	# Retrieves the URIs for all inducers used in the specified collection of experiments
	# This collection is typically associated with a challenge problem
	def query_experiment_set_inducers(self, collection):
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

	# Retrieves the URIs for all plasmids used in the specified collection of experiments
	# This collection is typically associated with a challenge problem
	def query_experiment_set_plasmids(self, collection):
		plasmid_query = """
		PREFIX sbol: <http://sbols.org/v2#>
		PREFIX sd2: <http://sd2e.org#>
		PREFIX prov: <http://www.w3.org/ns/prov#> 
		SELECT DISTINCT ?plasmid WHERE {{ 
  			{col} sbol:member ?exp .
  			?exp sd2:experimentalData ?data .
  			?data prov:wasDerivedFrom ?sample .
  			?sample sd2:built ?condition .
  			?condition sbol:functionalComponent ?fc .
  			?fc sbol:definition ?plasmid .
  			?plasmid sbol:type ?type1;
           		sbol:type ?type2 .
  		FILTER ( ?type1 = <http://www.biopax.org/release/biopax-level3.owl#DnaRegion> && 
  			?type2 = <http://identifiers.org/so/SO:0000988> )
		}}
		""".format(col=collection)

		return fetch_SPARQL(self.__server, plasmid_query)

	# Retrieves the URIs for all strains used in the specified collection of experiments
	# This collection is typically associated with a challenge problem
	def query_experiment_set_strains(self, collection):
		strain_query = """
		PREFIX sbol: <http://sbols.org/v2#>
		PREFIX sd2: <http://sd2e.org#>
		PREFIX prov: <http://www.w3.org/ns/prov#> 
		SELECT DISTINCT ?strain WHERE {{ 
  			{col} sbol:member ?exp .
  			?exp sd2:experimentalData ?data .
  			?data prov:wasDerivedFrom ?sample .
  			?sample sd2:built ?condition .
  			?condition sbol:functionalComponent ?fc .
  			?fc sbol:definition ?strain .
  			?strain sbol:type ?type .
  		FILTER ( ?type = <http://purl.obolibrary.org/obo/NCIT_C14419> || 
  			?type = <http://purl.obolibrary.org/obo/OBI_0001185> )
		}}
		""".format(col=collection)

		return fetch_SPARQL(self.__server, strain_query)

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
		PREFIX sbol: <http://sbols.org/v2#>
		PREFIX sd2: <http://sd2e.org#>
		PREFIX prov: <http://www.w3.org/ns/prov#> 
		SELECT DISTINCT ?plasmid WHERE {{ 
  			{exp} sd2:experimentalData ?data .
  			?data prov:wasDerivedFrom ?sample .
  			?sample sd2:built ?condition .
  			?condition sbol:functionalComponent ?fc .
  			?fc sbol:definition ?plasmid .
  			?plasmid sbol:type ?type1;
           		sbol:type ?type2 .
  		FILTER ( ?type1 = <http://www.biopax.org/release/biopax-level3.owl#DnaRegion> && 
  			?type2 = <http://identifiers.org/so/SO:0000988> )
		}}
		""".format(exp=experiment)

		return fetch_SPARQL(self.__server, plasmid_query)

	# Retrieves the URIs for all inducers in the specified experiment
	def query_experiment_strains(self, experiment):
		strains_query = """
		PREFIX sbol: <http://sbols.org/v2#>
		PREFIX sd2: <http://sd2e.org#>
		PREFIX prov: <http://www.w3.org/ns/prov#> 
		SELECT DISTINCT ?strain WHERE {{ 
  			{exp} sd2:experimentalData ?data .
  			?data prov:wasDerivedFrom ?sample .
  			?sample sd2:built ?condition .
  			?condition sbol:functionalComponent ?fc .
  			?fc sbol:definition ?strain .
  			?strain sbol:type ?type .
  		FILTER ( ?type = <http://purl.obolibrary.org/obo/NCIT_C14419> || 
  			?type = <http://purl.obolibrary.org/obo/OBI_0001185> ) 
		}}
		""".format(exp=experiment)

		return fetch_SPARQL(self.__server, strains_query)

	# Retrieves the source URLs for all experimental data files generated by the specified experiment
	def query_experiment_data(self, experiment):
		exp_data_query = """
		PREFIX sd2: <http://sd2e.org#>
		SELECT DISTINCT ?source WHERE {{ 
  			{exp} sd2:experimentalData ?data .
  			?data sd2:attachment ?attach .
  			?attach sd2:source ?source  
		}}
		""".format(exp=experiment)

		return fetch_SPARQL(self.__server, exp_data_query)

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

		return fetch_SPARQL(self.__server, sample_query)

	# Submit the data stored in the given sbolDoc to a collection on SynBioHub
	# sbh_connector: An instance of the pySBOL Partshop to set SynBioHub credential needed for submitting a collection
	# sbolDoc: The SBOL Document containing the data to be submitted to SynBioHub
	# isNewCollection: A boolean variable. True will submit the given sbolDoc to a new SynBioHub Collection. 
	# 	Otherwise, False will submit to existing SynBioHub Collection.
	# overwrite: An integer variable to indicate whether the data submitting to the existing SynBioHub collection should override information.
	# 	Note: Setting the variable overwrite = 1 (ovewrite existing collection data) or 2 (merge existing collection data with new data)
	def submit_Collection(self, sbh_connector, sbolDoc, isNewCollection, overwrite):
		result = sbh_connector.submit(sbolDoc) if isNewCollection else sbh_connector.submit(sbolDoc, sbolDoc.identity, overwrite)
		
		# SynBioHub will alert user if they have successfully uploaded their SBOL design. 
		# If uploading was not successful, errors or warnings will be stored in the result variable
		print(result)
		if result != 'Successfully uploaded':
			sys.exit(0)

	def login_SBH(self):
		sbh_connector = PartShop(self.__server)
		sbh_user = input('Enter SynBioHub Username: ')
		sbh_connector.login(sbh_user, getpass.getpass(prompt='Enter SynBioHub Password: ', stream=sys.stderr))
		return sbh_connector

	# Submit a new collection to the specified SynBioHub instance. 
	# sbolDoc: The SBOL Document containing SBOL parts that the user would like to upload as a new Collection.
	# displayId: The SynBioHub Collection Id that must be set when creating a new SynBioHub Collection. 
	# 	Note: This displayId must be unique from the Collection IDs that exist in the SynBioHub instance that the user want to upload their design to.
	# name: The SynBioHub Collection Name that must be set when creating a new SynBioHub Collection
	# description: A description about this new collection. 
	# version: The version number that you would like to set this new SynBioHub Collection as. 
	def submit_NewCollection(self, sbolDoc, displayId, name, description, version):
		# Set the required properties for the new SynBioHub collection
		sbolDoc.displayId = displayId
		sbolDoc.name = name
		sbolDoc.version = version
		sbolDoc.description = description
		sbh_connector = self.login_SBH()
		self.submit_Collection(sbh_connector, sbolDoc, True, 0)

	# Submit the given SBOL Document to an existing SynBioHub Collection
	# sbolDoc: The SBOL Document that the user wants to submit to the existing SynBioHub Collection
	# collURI: The URI of the SynBioHub Collection that the user would like to submit to
	# ovewrite: An integer variable to indicate whether the data submitting to the existing SynBioHub collection should override information.
	# 	Note: Setting the variable overwrite = 1 (ovewrite existing collection data) or 2 (merge existing collection data with new data). 0 will be set as default.
	def submit_ExistingCollection(self, sbolDoc, collURI, overwrite):
		sbolDoc.identity = collURI
		sbh_connector = self.login_SBH()
		self.submit_Collection(sbh_connector, sbolDoc, False, overwrite)