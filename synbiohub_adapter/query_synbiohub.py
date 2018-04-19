import getpass
import sys

from .fetch_SPARQL import fetch_SPARQL
from synbiohub_adapter.SynBioHubUtil import *
from sbol import *

''' 
	This module is used to query information from SD2's SynBioHub instance for DARPA's SD2E project.
	
	author(s) : Nicholas Roehner 
				Tramy Nguyen
''' 
class SynBioHubQuery(SBOLQuery):
	''' This class is used is used to push and pull information from SynBioHub.
		Each method of this class is a SPARQL query used to call to the specified instance of SynBioHub.
	'''

	# server: The SynBioHub server to call sparql queries on.
	def __init__(self, server):
		SBOLQuery.__init__(self, server)

	# Control query methods \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

	# Retrieves the URIs for all controls from the specified collection of design elements.
	# This collection is typically associated with a challenge problem.
	def query_design_set_controls(self, collection, sub_types=[], sub_roles=[], sub_definitions=[]):
		return self.query_design_set_modules(collection, [SBOLConstants.CONTROL], sub_types, sub_roles, sub_definitions)

	# Retrieves the URIs for all fluorescent bead controls from the specified collection of design elements.
	# This collection is typically associated with a challenge problem.
	def query_design_set_fbead_controls(self, collection):
		return self.query_design_set_controls(collection, [SBOLConstants.BEAD], [SBOLConstants.FLUORESCENT_PROBE])

	# Retrieves the URIs for all fluorescein controls from the specified collection of design elements.
	# This collection is typically associated with a challenge problem.
	def query_design_set_fluorescein_controls(self, collection):
		return self.query_design_set_controls(collection, [SBOLConstants.FLUORESCEIN])

	# Retrieves the URIs for all LUDOX controls from the specified collection of design elements.
	# This collection is typically associated with a challenge problem.
	def query_design_set_ludox_controls(self, collection):
		return self.query_design_set_controls(collection=collection, sub_definitions=[SD2Constants.LUDOX])

	# Retrieves the URIs for all water controls from the specified collection of design elements.
	# This collection is typically associated with a challenge problem.
	def query_design_set_water_controls(self, collection):
		return self.query_design_set_controls(collection, [SBOLConstants.H2O])

	# Retrieves the URIs for all controls from the collection of every SD2 design element.
	def query_design_controls(self, sub_types=[], sub_roles=[]):
		return self.query_design_set_controls(SD2Constants.SD2_DESIGN_COLLECTION, sub_types, sub_roles)

	# Retrieves the URIs for all fluorescent bead controls from the collection of every SD2 design element.
	def query_design_fbead_controls(self):
		return self.query_design_set_fbead_controls(SD2Constants.SD2_DESIGN_COLLECTION)

	# Retrieves the URIs for all water controls from the collection of every SD2 design element.
	def query_design_fluorescein_controls(self):
		return self.query_design_set_fluorescein_controls(SD2Constants.SD2_DESIGN_COLLECTION)

	# Retrieves the URIs for all fluorescent bead controls from the collection of every SD2 design element.
	def query_design_ludox_controls(self):
		return self.query_design_set_ludox_controls(SD2Constants.SD2_DESIGN_COLLECTION)

	# Retrieves the URIs for all water controls from the collection of every SD2 design element.
	def query_design_water_controls(self):
		return self.query_design_set_water_controls(SD2Constants.SD2_DESIGN_COLLECTION)

	# Gate query methods \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

	# Retrieves the URIs for all logic gates fom the specified collection of design elements.
	# This collection is typically associated with a challenge problem.
	def query_design_set_gates(self, collection):
		return self.query_design_set_modules(collection, [SBOLConstants.LOGIC_OPERATOR])

	# Retrieves the URIs for all logic gates from the collection of every SD2 design element.
	def query_design_gates(self):
		return self.query_design_set_gates(SD2Constants.SD2_DESIGN_COLLECTION)

	# Retrieves the URIs for all logic gates used in the specified experiment.
	def query_single_experiment_gates(self, experiment):
		gate_query = """
		PREFIX sbol: <http://sbols.org/v2#>
		PREFIX sd2: <http://sd2e.org#>
		PREFIX prov: <http://www.w3.org/ns/prov#> 
		SELECT DISTINCT ?gate WHERE {{ 
  			<{exp}> sd2:experimentalData ?data .
  			?data prov:wasDerivedFrom ?sample .
  			?sample sbol:built ?condition .
  			?condition sbol:module ?mod .
  			?mod sbol:definition ?gate .
  			?gate sbol:role <{ro}>
		}}
		""".format(exp=experiment, ro=SBOLConstants.LOGIC_OPERATOR)

		return fetch_SPARQL(self._SBOLQuery__server, gate_query)

	# Retrieves the URIs for all logic gates used in the specified collection of experiments.
	# This collection is typically associated with a challenge problem.
	def query_experiment_set_gates(self, collection):
		gate_query = """
		PREFIX sbol: <http://sbols.org/v2#>
		PREFIX sd2: <http://sd2e.org#>
		PREFIX prov: <http://www.w3.org/ns/prov#>
		SELECT DISTINCT ?gate WHERE {{ 
  			<{col}> sbol:member ?exp .
  			?exp sd2:experimentalData ?data .
  			?data prov:wasDerivedFrom ?sample .
  			?sample sbol:built ?condition .
  			?condition sbol:module ?mod .
  			?mod sbol:definition ?gate .
  			?gate sbol:role <{ro}>
		}}
		""".format(col=collection, ro=SBOLConstants.LOGIC_OPERATOR)

		return fetch_SPARQL(self._SBOLQuery__server, gate_query)

	# Retrieves the URIs for all logic gates used by experiments in the collection of every SD2 experiment.
	def query_experiment_gates(self):
		return self.query_experiment_set_gates(SD2Constants.SD2_EXPERIMENT_COLLECTION)

	# Inducer query methods \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

	# Retrieves the URIs for all inducers from the specified collection of design elements.
	# This collection is typically associated with a challenge problem.
	def query_design_set_inducers(self, collection):
		inducer_query = """
		PREFIX sbol: <http://sbols.org/v2#>
		SELECT DISTINCT ?inducer WHERE {{ 
  			<{col}> sbol:member ?inducer .
  			?inducer sbol:type <{ty}> ;
           		sbol:role <{ro}>
		}}
		""".format(col=collection, ty=BIOPAX_SMALL_MOLECULE, ro=SBOLConstants.EFFECTOR)

		return fetch_SPARQL(self._SBOLQuery__server, inducer_query)
	
	# Retrieves the URIs for all inducers from the collection of every SD2 design element.
	def query_design_inducers(self):
		return self.query_design_set_inducers(SD2Constants.SD2_DESIGN_COLLECTION)

	# Retrieves the URIs for all inducers in the specified experiment and their associated levels.
	def query_single_experiment_inducers(self, experiment):
		inducer_query = """
		PREFIX sbol: <http://sbols.org/v2#>
		PREFIX sd2: <http://sd2e.org#>
		PREFIX om: <http://www.ontology-of-units-of-measure.org/resource/om-2#>
		PREFIX prov: <http://www.w3.org/ns/prov#> 
		SELECT ?inducer (concat('[',group_concat(distinct ?level;separator=','),']') as ?levels)
		WHERE {{ 
  			<{exp}> sd2:experimentalData ?data .
  			?data prov:wasDerivedFrom ?sample .
  			?sample sbol:built ?condition .
  			?condition sbol:functionalComponent ?fc .
  			?fc sbol:definition ?inducer .
  			?inducer sbol:type <{ty}> ;
           		sbol:role <{ro}> .
           	OPTIONAL {{ 
           		?fc om:measure ?concentration .
           		?concentration om:hasNumericalValue ?level
           	}}
		}}
		GROUP BY ?inducer
		""".format(exp=experiment, ty=BIOPAX_SMALL_MOLECULE, ro=SBOLConstants.EFFECTOR)

		return fetch_SPARQL(self._SBOLQuery__server, inducer_query)

	# Retrieves the URIs for all inducers used in the specified collection of experiments and their associated levels.
	# This collection is typically associated with a challenge problem.
	def query_experiment_set_inducers(self, collection):
		inducer_query = """
		PREFIX sbol: <http://sbols.org/v2#>
		PREFIX sd2: <http://sd2e.org#>
		PREFIX om: <http://www.ontology-of-units-of-measure.org/resource/om-2#>
		PREFIX prov: <http://www.w3.org/ns/prov#> 
		SELECT ?inducer (concat('[',group_concat(distinct ?level;separator=','),']') as ?levels)
		WHERE {{ 
  			<{col}> sbol:member ?exp .
  			?exp sd2:experimentalData ?data .
  			?data prov:wasDerivedFrom ?sample .
  			?sample sbol:built ?condition .
  			?condition sbol:functionalComponent ?fc .
  			?fc sbol:definition ?inducer .
  			?inducer sbol:type <{ty}> ;
           		sbol:role <{ro}> .
           	OPTIONAL {{ 
           		?fc om:measure ?concentration .
           		?concentration om:hasNumericalValue ?level
           	}}
		}}
		GROUP BY ?inducer
		""".format(col=collection, ty=BIOPAX_SMALL_MOLECULE, ro=SBOLConstants.EFFECTOR)

		return fetch_SPARQL(self._SBOLQuery__server, inducer_query)

	# Retrieves the URIs for all inducers used by experiments in the collection of every SD2 experiment.
	def query_experiment_inducers(self):
		return self.query_experiment_set_inducers(SD2Constants.SD2_EXPERIMENT_COLLECTION)

	# Retrieves the URIs for all inducers in the specified sample and their associated levels.
	def query_sample_inducers(self, sample):
		inducer_query = """
		PREFIX sbol: <http://sbols.org/v2#>
		PREFIX om: <http://www.ontology-of-units-of-measure.org/resource/om-2#>
		SELECT ?inducer ?level WHERE {{ 
  			<{samp}> sbol:built ?condition .
  			?condition sbol:functionalComponent ?fc .
  			?fc sbol:definition ?inducer .
  			?inducer sbol:type <{ty}> ;
           		sbol:role <{ro}> .
           	OPTIONAL {{ 
           		?fc om:measure ?concentration .
           		?concentration om:hasNumericalValue ?level
           	}}
		}}
		GROUP BY ?inducer
		""".format(samp=sample, ty=BIOPAX_SMALL_MOLECULE, ro=SBOLConstants.EFFECTOR)

		return fetch_SPARQL(self._SBOLQuery__server, inducer_query)

	# Retrieves the URIs for all inducers in the specified sample condition and their associated levels.
	def query_condition_inducers(self, condition):
		inducer_query = """
		PREFIX sbol: <http://sbols.org/v2#>
		PREFIX om: <http://www.ontology-of-units-of-measure.org/resource/om-2#>
		SELECT ?inducer ?level WHERE {{ 
  			<{cond}> sbol:functionalComponent ?fc .
  			?fc sbol:definition ?inducer .
  			?inducer sbol:type <{ty}> ;
           		sbol:role <{ro}> .
           	OPTIONAL {{ 
           		?fc om:measure ?concentration .
           		?concentration om:hasNumericalValue ?level
           	}}
		}}
		GROUP BY ?inducer
		""".format(cond=condition, ty=BIOPAX_SMALL_MOLECULE, ro=SBOLConstants.EFFECTOR)

		return fetch_SPARQL(self._SBOLQuery__server, inducer_query)

	# Media query methods \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

	# Retrieves the URIs for all media from the specified collection of design elements.
	# This collection is typically associated with a challenge problem.
	def query_design_set_media(self, collection):
		return self.query_design_set_modules(collection, [SBOLConstants.MEDIA])

	# Retrieves the URIs for all media from the collection of every SD2 design element.
	def query_design_media(self):
		return self.query_design_set_media(SD2Constants.SD2_DESIGN_COLLECTION)

	# Plasmid query methods \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

	# Retrieves the URIs for all plasmids from the specified collection of design elements.
	# This collection is typically associated with a challenge problem.
	def query_design_set_plasmids(self, collection):
		return self.query_design_set_components(collection, [BIOPAX_DNA, SO_CIRCULAR])

	# Retrieves the URIs for all plasmids from the collection of every SD2 design element.
	def query_design_plasmids(self):
		return self.query_design_set_plasmids(SD2Constants.SD2_DESIGN_COLLECTION)

	# Retrieves the URIs for all plasmids in the specified experiment.
	def query_single_experiment_plasmids(self, experiment):
		plasmid_query = """
		PREFIX sbol: <http://sbols.org/v2#>
		PREFIX sd2: <http://sd2e.org#>
		PREFIX prov: <http://www.w3.org/ns/prov#> 
		SELECT DISTINCT ?plasmid WHERE {{ 
  			<{exp}> sd2:experimentalData ?data .
  			?data prov:wasDerivedFrom ?sample .
  			?sample sbol:built ?condition .
  			?condition sbol:functionalComponent ?fc .
  			?fc sbol:definition ?plasmid .
  			?plasmid sbol:type <{ty1}> ;
           		sbol:type <{ty2}>
		}}
		""".format(exp=experiment, ty1=BIOPAX_DNA, ty2=SO_CIRCULAR)

		return fetch_SPARQL(self._SBOLQuery__server, plasmid_query)

	# Retrieves the URIs for all plasmids used in the specified collection of experiments.
	# This collection is typically associated with a challenge problem.
	def query_experiment_set_plasmids(self, collection):
		plasmid_query = """
		PREFIX sbol: <http://sbols.org/v2#>
		PREFIX sd2: <http://sd2e.org#>
		PREFIX prov: <http://www.w3.org/ns/prov#> 
		SELECT DISTINCT ?plasmid WHERE {{ 
  			<{col}> sbol:member ?exp .
  			?exp sd2:experimentalData ?data .
  			?data prov:wasDerivedFrom ?sample .
  			?sample sbol:built ?condition .
  			?condition sbol:functionalComponent ?fc .
  			?fc sbol:definition ?plasmid .
  			?plasmid sbol:type <{ty1}> ;
           		sbol:type <{ty2}>
		}}
		""".format(col=collection, ty1=BIOPAX_DNA, ty2=SO_CIRCULAR)

		return fetch_SPARQL(self._SBOLQuery__server, plasmid_query)

	# Retrieves the URIs for all plasmids used by experiments in the collection of every SD2 experiment.
	def query_experiment_plasmids(self):
		return self.query_experiment_set_plasmids(SD2Constants.SD2_EXPERIMENT_COLLECTION)

	# Retrieves the URIs for all plasmids in the specified sample.
	def query_sample_plasmids(self, sample):
		plasmid_query = """
		PREFIX sbol: <http://sbols.org/v2#>
		SELECT DISTINCT ?plasmid WHERE {{ 
  			<{samp}> sbol:built ?condition .
  			?condition sbol:functionalComponent ?fc .
  			?fc sbol:definition ?plasmid .
  			?plasmid sbol:type <{ty1}> ;
           		sbol:type <{ty2}>
		}}
		""".format(samp=sample, ty1=BIOPAX_DNA, ty2=SO_CIRCULAR)

		return fetch_SPARQL(self._SBOLQuery__server, plasmid_query)

	# Retrieves the URIs for all plasmids in the specified sample condition.
	def query_condition_plasmids(self, condition):
		plasmid_query = """
		PREFIX sbol: <http://sbols.org/v2#>
		SELECT DISTINCT ?plasmid WHERE {{ 
  			<{cond}> sbol:functionalComponent ?fc .
  			?fc sbol:definition ?plasmid .
  			?plasmid sbol:type <{ty1}> ;
           		sbol:type <{ty2}>
		}}
		""".format(cond=condition, ty1=BIOPAX_DNA, ty2=SO_CIRCULAR)

		return fetch_SPARQL(self._SBOLQuery__server, plasmid_query)

	# Strain query methods \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

	# Retrieves the URIs for all strains from the specified collection of design elements.
	# This collection is typically associated with a challenge problem.
	def query_design_set_strains(self, collection):
		return self.query_design_set_components(collection=collection, types=[SBOLConstants.NCIT_STRAIN, SBOLConstants.OBI_STRAIN], all_types=False)

	# Retrieves the URIs for all strains from the collection of every SD2 design element.
	def query_design_strains(self):
		return self.query_design_set_strains(SD2Constants.SD2_DESIGN_COLLECTION)

	# Retrieves the URIs for all inducers in the specified experiment.
	def query_single_experiment_strains(self, experiment):
		strains_query = """
		PREFIX sbol: <http://sbols.org/v2#>
		PREFIX sd2: <http://sd2e.org#>
		PREFIX prov: <http://www.w3.org/ns/prov#> 
		SELECT DISTINCT ?strain WHERE {{
  			<{exp}> sd2:experimentalData ?data .
  			?data prov:wasDerivedFrom ?sample .
  			?sample sbol:built ?condition .
  			?condition sbol:functionalComponent ?fc .
  			?fc sbol:definition ?strain .
  			VALUES (?type) {{ ( <{ty1}> ) ( <{ty2}> ) }}
  			?strain sbol:type ?type
		}}
		""".format(exp=experiment, ty1=SBOLConstants.NCIT_STRAIN, ty2=SBOLConstants.OBI_STRAIN)

		return fetch_SPARQL(self._SBOLQuery__server, strains_query)

	# Retrieves the URIs for all strains used in the specified collection of experiments.
	# This collection is typically associated with a challenge problem.
	def query_experiment_set_strains(self, collection):
		strain_query = """
		PREFIX sbol: <http://sbols.org/v2#>
		PREFIX sd2: <http://sd2e.org#>
		PREFIX prov: <http://www.w3.org/ns/prov#> 
		SELECT DISTINCT ?strain WHERE {{ 
  			<{col}> sbol:member ?exp .
  			?exp sd2:experimentalData ?data .
  			?data prov:wasDerivedFrom ?sample .
  			?sample sbol:built ?condition .
  			?condition sbol:functionalComponent ?fc .
  			?fc sbol:definition ?strain .
  			VALUES (?type) {{ ( <{ty1}> ) ( <{ty2}> ) }}
  			?strain sbol:type ?type
		}}
		""".format(col=collection, ty1=SBOLConstants.NCIT_STRAIN, ty2=SBOLConstants.OBI_STRAIN)

		return fetch_SPARQL(self._SBOLQuery__server, strain_query)

	# Retrieves the URIs for all strains used by experiments in the collection of every SD2 experiment.
	def query_experiment_strains(self):
		return self.query_experiment_set_strains(SD2Constants.SD2_EXPERIMENT_COLLECTION)

	# Experiment data query methods \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

	# Retrieves the source URLs for all experimental data files generated by the specified experiment and their associated samples.
	def query_single_experiment_data(self, experiment):
		exp_data_query = """
		PREFIX sd2: <http://sd2e.org#>
		PREFIX prov: <http://www.w3.org/ns/prov#> 
		SELECT ?sample (concat('[',group_concat(distinct ?source;separator=','),']') as ?sources)
		WHERE {{ 
  			<{exp}> sd2:experimentalData ?data .
  			?data prov:wasDerivedFrom ?sample;
  				sd2:attachment ?attach .
  			?attach sd2:source ?source
		}}
		""".format(exp=experiment)

		return fetch_SPARQL(self._SBOLQuery__server, exp_data_query)

	# Design and experiment set query methods \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

	# Retrieves the URIs for all sub-collections of design elements from the collection of every SD2 design element.
	# These sub-collections are typically associated with challenge problems.
	def query_design_sets(self):
		design_set_query = """
		PREFIX sbol: <http://sbols.org/v2#>
		SELECT DISTINCT ?collection WHERE {{ 
  			<{col}> sbol:member ?design ;
  				sbol:member ?collection .
  			?collection sbol:member ?design
		}}
		""".format(col=SD2Constants.SD2_DESIGN_COLLECTION)

		return fetch_SPARQL(self._SBOLQuery__server, design_set_query)

	# Retrieves the URIs for all sub-collections of experiments from the collection of every SD2 experiemnt.
	# These sub-collections are typically associated with challenge problems.
	def query_experiment_sets(self):
		exp_set_query = """
		PREFIX sbol: <http://sbols.org/v2#>
		PREFIX sd2: <http://sd2e.org#>
		SELECT DISTINCT ?subcol WHERE {{ 
  			<{col}> sbol:member ?subcol .
  			?subcol sbol:member ?exp .
  			?exp sd2:experimentalData ?data .
  			FILTER NOT EXISTS {{
  				?subcol sbol:member ?m .
  				FILTER ( ?m != ?exp )
  			}}
		}}
		""".format(col=SD2Constants.SD2_EXPERIMENT_COLLECTION)

		return fetch_SPARQL(self._SBOLQuery__server, exp_set_query)

	# Retrieves the size of the specified collection of experiments.
	# This collection is typically associated with a challenge problem.
	def query_experiment_set_size(self, collection):
		exp_set_size_query = """
		PREFIX sbol: <http://sbols.org/v2#>
		PREFIX sd2: <http://sd2e.org#>
		SELECT (count(distinct ?exp) as ?size) WHERE {{ 
  			<{col}> sbol:member ?exp .
  			?exp sd2:experimentalData ?data
		}}
		""".format(col=collection)

		return fetch_SPARQL(self._SBOLQuery__server, exp_set_size_query)

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
		sbh_connector = login_SBH(self._SBOLQuery__server)
		self.submit_Collection(sbh_connector, sbolDoc, True, 0)

	# Submit the given SBOL Document to an existing SynBioHub Collection
	# sbolDoc: The SBOL Document that the user wants to submit to the existing SynBioHub Collection
	# collURI: The URI of the SynBioHub Collection that the user would like to submit to
	# ovewrite: An integer variable to indicate whether the data submitting to the existing SynBioHub collection should override information.
	# 	Note: Setting the variable overwrite = 1 (ovewrite existing collection data) or 2 (merge existing collection data with new data). 0 will be set as default.
	def submit_ExistingCollection(self, sbolDoc, collURI, overwrite):
		sbolDoc.identity = collURI
		sbh_connector = login_SBH(self._SBOLQuery__server)
		self.submit_Collection(sbh_connector, sbolDoc, False, overwrite)
