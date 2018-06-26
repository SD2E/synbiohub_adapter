import getpass
import sys
import json

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
	def __init__(self, server, use_fallback_cache=False):
		super().__init__(server, use_fallback_cache)

	# Control query methods \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

	# Retrieves the URIs for all controls from the collection of every SD2 design element.
	def query_design_controls(self, verbose=False, pretty=False, collections=[SD2Constants.SD2_DESIGN_COLLECTION], sub_types=[], sub_roles=[], definitions=[], all_sub_types=True):
		mod_labels = ['control']

		if verbose:
			mod_labels.extend(['name', 'description'])

		query_result = self.query_design_modules([SBOLConstants.CONTROL], collections, mod_labels[0], mod_labels[1:], sub_types, sub_roles, definitions, all_sub_types)

		if pretty:
			return self.format_query_result(query_result, mod_labels)
		else:
			return query_result

	# Retrieves the URIs for all controls from the specified collection of design elements.
	# This collection is typically associated with a challenge problem.
	def query_design_set_controls(self, collection, verbose=False, pretty=False, sub_types=[], sub_roles=[], definitions=[]):
		return self.query_design_controls(verbose, pretty, [collection], sub_types, sub_roles, definitions)

	# Retrieves the URIs for all fluorescent bead controls from the collection of every SD2 design element.
	def query_design_fbead_controls(self, verbose=False, pretty=False, collections=[SD2Constants.SD2_DESIGN_COLLECTION]):
		return self.query_design_controls(verbose, pretty, collections, [SBOLConstants.BEAD], [SBOLConstants.FLUORESCENCE])

	# Retrieves the URIs for all fluorescent bead controls from the specified collection of design elements.
	# This collection is typically associated with a challenge problem.
	def query_design_set_fbead_controls(self, collection, verbose=False, pretty=False):
		return self.query_design_fbead_controls(verbose, pretty, [collection])

	# Retrieves the URIs for all water controls from the collection of every SD2 design element.
	def query_design_fluorescein_controls(self, verbose=False, pretty=False, collections=[SD2Constants.SD2_DESIGN_COLLECTION]):
		return self.query_design_controls(verbose, pretty, collections, [SBOLConstants.FLUORESCEIN])

	# Retrieves the URIs for all fluorescein controls from the specified collection of design elements.
	# This collection is typically associated with a challenge problem.
	def query_design_set_fluorescein_controls(self, collection, verbose=False, pretty=False):
		return self.query_design_fluorescein_controls(verbose, pretty, [collection])

	# Retrieves the URIs for all fluorescent bead controls from the collection of every SD2 design element.
	def query_design_ludox_controls(self, verbose=False, pretty=False, collections=[SD2Constants.SD2_DESIGN_COLLECTION]):
		return self.query_design_controls(verbose, pretty, collections, definitions=[SD2Constants.LUDOX])

	# Retrieves the URIs for all LUDOX controls from the specified collection of design elements.
	# This collection is typically associated with a challenge problem.
	def query_design_set_ludox_controls(self, collection, verbose=False, pretty=False):
		return self.query_design_ludox_controls(verbose, pretty, [collection])

	# Retrieves the URIs for all water controls from the collection of every SD2 design element.
	def query_design_water_controls(self, verbose=False, pretty=False, collections=[SD2Constants.SD2_DESIGN_COLLECTION]):
		return self.query_design_controls(verbose, pretty, collections, [SBOLConstants.H2O])

	# Retrieves the URIs for all water controls from the specified collection of design elements.
	# This collection is typically associated with a challenge problem.
	def query_design_set_water_controls(self, collection, verbose=False, pretty=False):
		return self.query_design_water_controls(verbose, pretty, [collection])

	# Retrieves the URIs for all controls used by experiments in the collection of every SD2 experiment.
	def query_experiment_controls(self, verbose=False, trace_derivation=True, by_sample=False, pretty=True, collections=[SD2Constants.SD2_EXPERIMENT_COLLECTION], sub_types=[], sub_roles=[], definitions=[], all_sub_types=True, experiments=[]):
		mod_labels = ['control']

		if verbose:
			mod_labels.extend(['name', 'description'])

		if by_sample:
			mod_labels.append('sample')

		query_result = self.query_experiment_modules([SBOLConstants.CONTROL], collections, mod_labels[0], mod_labels[1:], trace_derivation, sub_types, sub_roles, definitions, all_sub_types, experiments)

		if pretty:
			if by_sample:
				return self.format_query_result(query_result, mod_labels[:-1], mod_labels[-1])
			else:
				return self.format_query_result(query_result, mod_labels)
		else:
			return query_result

	# Retrieves the URIs for all controls used in the specified collection of experiments.
	# This collection is typically associated with a challenge problem.
	def query_experiment_set_controls(self, collection, verbose=False, trace_derivation=False, by_sample=False, pretty=True):
		return self.query_experiment_controls(verbose, trace_derivation, by_sample, pretty, [collection])

	# Retrieves the URIs for all controls used in the specified experiment.
	def query_single_experiment_controls(self, experiment, verbose=False, trace_derivation=True, by_sample=True, pretty=True):
		return self.query_experiment_controls(verbose, trace_derivation, by_sample, pretty, experiments=[experiment])

	# Retrieves the URIs for all controls used by experiments in the collection of every SD2 experiment.
	def query_experiment_fbead_controls(self, verbose=False, trace_derivation=True, by_sample=False, pretty=True, collections=[SD2Constants.SD2_EXPERIMENT_COLLECTION], experiments=[]):
		return self.query_experiment_controls(verbose, trace_derivation, by_sample, pretty, collections, [SBOLConstants.BEAD], [SBOLConstants.FLUORESCENCE], experiments=experiments)

	# Retrieves the URIs for all controls used in the specified collection of experiments.
	# This collection is typically associated with a challenge problem.
	def query_experiment_set_fbead_controls(self, collection, verbose=False, trace_derivation=True, by_sample=False, pretty=True):
		return self.query_experiment_fbead_controls(verbose, trace_derivation, by_sample, pretty, [collection])

	# Retrieves the URIs for all controls used in the specified experiment.
	def query_single_experiment_fbead_controls(self, experiment, verbose=False, trace_derivation=True, by_sample=True, pretty=True):
		return self.query_experiment_fbead_controls(verbose, trace_derivation, by_sample, pretty, experiments=[experiment])

	# Retrieves the URIs for all controls used by experiments in the collection of every SD2 experiment.
	def query_experiment_fluorescein_controls(self, verbose=False, trace_derivation=True, by_sample=False, pretty=True, collections=[SD2Constants.SD2_EXPERIMENT_COLLECTION], experiments=[]):
		return self.query_experiment_controls(verbose, trace_derivation, by_sample, pretty, collections, [SBOLConstants.FLUORESCEIN], experiments=experiments)

	# Retrieves the URIs for all controls used in the specified collection of experiments.
	# This collection is typically associated with a challenge problem.
	def query_experiment_set_fluorescein_controls(self, collection, verbose=False, trace_derivation=True, by_sample=False, pretty=True):
		return self.query_experiment_fluorescein_controls(verbose, trace_derivation, by_sample, pretty, [collection])

	# Retrieves the URIs for all controls used in the specified experiment.
	def query_single_experiment_fluorescein_controls(self, experiment, verbose=False, trace_derivation=True, by_sample=True, pretty=True):
		return self.query_experiment_fluorescein_controls(verbose, trace_derivation, by_sample, pretty, experiments=[experiment])

	# Retrieves the URIs for all controls used by experiments in the collection of every SD2 experiment.
	def query_experiment_ludox_controls(self, verbose=False, trace_derivation=True, by_sample=False, pretty=True, collections=[SD2Constants.SD2_EXPERIMENT_COLLECTION], experiments=[]):
		return self.query_experiment_controls(verbose, trace_derivation, by_sample, pretty, collections, definitions=[SD2Constants.LUDOX], experiments=experiments)

	# Retrieves the URIs for all controls used in the specified collection of experiments.
	# This collection is typically associated with a challenge problem.
	def query_experiment_set_ludox_controls(self, collection, verbose=False, trace_derivation=True, by_sample=False, pretty=True):
		return self.query_experiment_ludox_controls(verbose, trace_derivation, by_sample, pretty, [collection])

	# Retrieves the URIs for all controls used in the specified experiment.
	def query_single_experiment_ludox_controls(self, experiment, verbose=False, trace_derivation=True, by_sample=True, pretty=True):
		return self.query_experiment_ludox_controls(verbose, trace_derivation, by_sample, pretty, experiments=[experiment])

	# Retrieves the URIs for all controls used by experiments in the collection of every SD2 experiment.
	def query_experiment_water_controls(self, verbose=False, trace_derivation=True, by_sample=False, pretty=True, collections=[SD2Constants.SD2_EXPERIMENT_COLLECTION], experiments=[]):
		return self.query_experiment_controls(verbose, trace_derivation, by_sample, pretty, collections, [SBOLConstants.H2O], experiments=experiments)

	# Retrieves the URIs for all controls used in the specified collection of experiments.
	# This collection is typically associated with a challenge problem.
	def query_experiment_set_water_controls(self, collection, verbose=False, trace_derivation=True, by_sample=False, pretty=True):
		return self.query_experiment_water_controls(verbose, trace_derivation, by_sample, pretty, [collection])

	# Retrieves the URIs for all controls used in the specified experiment.
	def query_single_experiment_water_controls(self, experiment, verbose=False, trace_derivation=True, by_sample=True, pretty=True):
		return self.query_experiment_water_controls(verbose, trace_derivation, by_sample, pretty, experiments=[experiment])

	# Gate query methods \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

	# Retrieves the URIs for all logic gates from the collection of every SD2 design element.
	def query_design_gates(self, verbose=False, with_role=True, pretty=False, collections=[SD2Constants.SD2_DESIGN_COLLECTION]):
		mod_labels = ['gate']

		if verbose:
			mod_labels.extend(['name', 'description'])

		if with_role:
			mod_labels.append('role')

		query_result = self.query_design_modules(SD2Constants.LOGIC_OPERATORS, collections, mod_labels[0], mod_labels[1:])

		if pretty:
			return self.format_query_result(query_result, mod_labels)
		else:
			return query_result

	# Retrieves the URIs for all logic gates fom the specified collection of design elements.
	# This collection is typically associated with a challenge problem.
	def query_design_set_gates(self, collection, verbose=False, with_role=True, pretty=False):
		return self.query_design_gates(verbose, with_role, [collection])

	# Retrieves the URIs for all logic gates used by experiments in the collection of every SD2 experiment.
	def query_experiment_gates(self, verbose=False, with_role=True, trace_derivation=True, by_sample=False, pretty=True, collections=[SD2Constants.SD2_EXPERIMENT_COLLECTION], experiments=[]):
		mod_labels = ['gate']

		if verbose:
			mod_labels.extend(['name', 'description'])

		if with_role:
			mod_labels.append('role')

		if by_sample:
			mod_labels.append('sample')

		query_result = self.query_experiment_modules(SD2Constants.LOGIC_OPERATORS, collections, mod_labels[0], mod_labels[1:], trace_derivation, experiments=experiments)

		if pretty:
			if by_sample:
				return self.format_query_result(query_result, mod_labels[:-1], mod_labels[-1])
			else:
				return self.format_query_result(query_result, mod_labels)
		else:
			return query_result

	# Retrieves the URIs for all logic gates used in the specified collection of experiments.
	# This collection is typically associated with a challenge problem.
	def query_experiment_set_gates(self, collection, verbose=False, with_role=True, trace_derivation=True, by_sample=False, pretty=True):
		return self.query_experiment_gates(verbose, with_role, trace_derivation, by_sample, pretty, [collection])

	# Retrieves the URIs for all logic gates used in the specified experiment.
	def query_single_experiment_gates(self, experiment, verbose=False, with_role=True, trace_derivation=True, by_sample=True, pretty=True):
		return self.query_experiment_gates(verbose, with_role, trace_derivation, by_sample, pretty, experiments=[experiment])

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
    
		return self.fetch_SPARQL(self._server, inducer_query)
	
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

		return self.fetch_SPARQL(self._server, inducer_query)

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

		return self.fetch_SPARQL(self._server, inducer_query)

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

		return self.fetch_SPARQL(self._server, inducer_query)

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

		return self.fetch_SPARQL(self._server, inducer_query)

	# Media query methods \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

	# Retrieves the URIs for all media from the collection of every SD2 design element.
	def query_design_media(self, verbose=False, pretty=False, collections=[SD2Constants.SD2_DESIGN_COLLECTION]):
		mod_labels = ['media']

		if verbose:
			mod_labels.extend(['name', 'description'])

		query_result = self.query_design_modules([SBOLConstants.MEDIA], collections, mod_labels[0], mod_labels[1:])

		if pretty:
			return self.format_query_result(query_result, mod_labels)
		else:
			return query_result

	# Retrieves the URIs for all media from the specified collection of design elements.
	# This collection is typically associated with a challenge problem.
	def query_design_set_media(self, collection, verbose=False, pretty=False):
		return self.query_design_media(verbose, pretty, [collection])

	# Retrieves the URIs for all media used by experiments in the collection of every SD2 experiment.
	def query_experiment_media(self, verbose=False, trace_derivation=True, by_sample=False, pretty=True, collections=[SD2Constants.SD2_EXPERIMENT_COLLECTION], experiments=[]):
		mod_labels = ['media']

		if verbose:
			mod_labels.extend(['name', 'description'])

		if by_sample:
			mod_labels.append('sample')

		query_result = self.query_experiment_modules([SBOLConstants.MEDIA], collections, mod_labels[0], mod_labels[1:], trace_derivation, experiments=experiments)

		if pretty:
			if by_sample:
				return self.format_query_result(query_result, mod_labels[:-1], mod_labels[-1])
			else:
				return self.format_query_result(query_result, mod_labels)
		else:
			return query_result

	# Retrieves the URIs for all media used in the specified collection of experiments.
	# This collection is typically associated with a challenge problem.
	def query_experiment_set_media(self, collection, verbose=False, trace_derivation=True, by_sample=False, pretty=True):
		return self.query_experiment_media(verbose, trace_derivation, by_sample, pretty, [collection])

	# Retrieves the URIs for all media used in the specified experiment.
	def query_single_experiment_media(self, experiment, verbose=False, trace_derivation=True, by_sample=True, pretty=True):
		return self.query_experiment_media(verbose, trace_derivation, by_sample, pretty, experiments=[experiment])

	# Plasmid query methods \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

	# Retrieves the URIs for all plasmids from the collection of every SD2 design element.
	def query_design_plasmids(self, verbose=False, with_sequence=False, pretty=False, collections=[SD2Constants.SD2_DESIGN_COLLECTION]):
		comp_labels = ['plasmid']

		if verbose:
			comp_labels.extend(['name', 'description'])

		if with_sequence:
			comp_labels.append('sequence')

		query_result = self.query_design_components([BIOPAX_DNA, SO_CIRCULAR], collections, comp_labels[0], comp_labels[1:])

		if pretty:
			return self.format_query_result(query_result, comp_labels)
		else:
			return query_result

	# Retrieves the URIs for all plasmids from the specified collection of design elements.
	# This collection is typically associated with a challenge problem.
	def query_design_set_plasmids(self, collection, verbose=False, with_sequence=False, pretty=False):
		return self.query_design_plasmids(verbose, with_sequence, pretty, [collection])

	# Retrieves the URIs for all plasmids used by experiments in the collection of every SD2 experiment.
	def query_experiment_plasmids(self, verbose=False, with_sequence=False, trace_derivation=True, by_sample=False, pretty=True, collections=[SD2Constants.SD2_EXPERIMENT_COLLECTION], experiments=[]):
		comp_labels = ['plasmid']

		if verbose:
			comp_labels.extend(['name', 'description'])

		if with_sequence:
			comp_labels.append('sequence')

		if by_sample:
			comp_labels.append('sample')

		query_result = self.query_experiment_components([BIOPAX_DNA, SO_CIRCULAR], collections, comp_labels[0], comp_labels[1:], trace_derivation, experiments=experiments)

		if pretty:
			if by_sample:
				return self.format_query_result(query_result, comp_labels[:-1], comp_labels[-1])
			else:
				return self.format_query_result(query_result, comp_labels)
		else:
			return query_result

	# Retrieves the URIs for all plasmids used in the specified collection of experiments.
	# This collection is typically associated with a challenge problem.
	def query_experiment_set_plasmids(self, collection, verbose=False, with_sequence=False, trace_derivation=True, by_sample=False, pretty=True):
		return self.query_experiment_plasmids(verbose, with_sequence, trace_derivation, by_sample, pretty, [collection])

	# Retrieves the URIs for all plasmids in the specified experiment.
	def query_single_experiment_plasmids(self, experiment, verbose=False, with_sequence=False, trace_derivation=True, by_sample=True, pretty=True):
		return self.query_experiment_plasmids(verbose, with_sequence, trace_derivation, by_sample, pretty, experiments=[experiment])

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

		return self.fetch_SPARQL(self._server, plasmid_query)

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

		return self.fetch_SPARQL(self._server, plasmid_query)

	# Plasmid query methods \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

	# Retrieves the URIs for all riboswitches from the collection of every SD2 design element.
	def query_design_riboswitches(self, verbose=False, with_sequence=False, pretty=False, collections=[SD2Constants.SD2_DESIGN_COLLECTION]):
		comp_labels = ['riboswitch']

		if verbose:
			comp_labels.extend(['name', 'description'])

		if with_sequence:
			comp_labels.append('sequence')

		query_result = self.query_design_components([BIOPAX_DNA], collections, comp_labels[0], comp_labels[1:], [SBOLConstants.RIBOSWITCH])

		if pretty:
			return self.format_query_result(query_result, comp_labels)
		else:
			return query_result

	# Retrieves the URIs for all riboswitches from the specified collection of design elements.
	# This collection is typically associated with a challenge problem.
	def query_design_set_riboswitches(self, collection, verbose=False, with_sequence=False, pretty=False):
		return self.query_design_riboswitches(verbose, with_sequence, pretty, [collection])

	# Retrieves the URIs for all riboswitches used by experiments in the collection of every SD2 experiment.
	def query_experiment_riboswitches(self, verbose=False, with_sequence=False, trace_derivation=True, by_sample=False, pretty=True, collections=[SD2Constants.SD2_EXPERIMENT_COLLECTION], experiments=[]):
		comp_labels = ['riboswitch']

		if verbose:
			comp_labels.extend(['name', 'description'])

		if with_sequence:
			comp_labels.append('sequence')

		if by_sample:
			comp_labels.append('sample')

		query_result = self.query_experiment_components([BIOPAX_DNA], collections, comp_labels[0], comp_labels[1:], trace_derivation, [SBOLConstants.RIBOSWITCH], experiments=experiments)

		if pretty:
			if by_sample:
				return self.format_query_result(query_result, comp_labels[:-1], comp_labels[-1])
			else:
				return self.format_query_result(query_result, comp_labels)
		else:
			return query_result

	# Retrieves the URIs for all riboswitches used in the specified collection of experiments.
	# This collection is typically associated with a challenge problem.
	def query_experiment_set_riboswitches(self, collection, verbose=False, with_sequence=False, trace_derivation=True, by_sample=False, pretty=True):
		return self.query_experiment_riboswitches(verbose, with_sequence, trace_derivation, by_sample, pretty, [collection])

	# Retrieves the URIs for all riboswitches in the specified experiment.
	def query_single_experiment_riboswitches(self, experiment, verbose=False, with_sequence=False, trace_derivation=True, by_sample=True, pretty=True):
		return self.query_experiment_riboswitches(verbose, with_sequence, trace_derivation, by_sample, pretty, experiments=[experiment])

	# Strain query methods \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

	# Retrieves the URIs for all strains from the collection of every SD2 design element.
	def query_design_strains(self, verbose=False, pretty=False, collections=[SD2Constants.SD2_DESIGN_COLLECTION]):
		comp_labels = ['strain']

		if verbose:
			comp_labels.extend(['name', 'description'])

		query_result = self.query_design_components([SBOLConstants.NCIT_STRAIN, SBOLConstants.OBI_STRAIN], collections, comp_labels[0], comp_labels[1:], all_types=False)

		if pretty:
			return self.format_query_result(query_result, comp_labels)
		else:
			return query_result
		
	# Retrieves the URIs for all strains from the specified collection of design elements.
	# This collection is typically associated with a challenge problem.
	def query_design_set_strains(self, collection, verbose=False, pretty=False):
		return self.query_design_strains(verbose, pretty, [collection])

	# Retrieves the URIs for all strains used by experiments in the collection of every SD2 experiment.
	def query_experiment_strains(self, verbose=False, trace_derivation=True, by_sample=False, pretty=True, collections=[SD2Constants.SD2_EXPERIMENT_COLLECTION], experiments=[]):
		comp_labels = ['strain']

		if verbose:
			comp_labels.extend(['name', 'description'])

		if by_sample:
			comp_labels.append('sample')

		query_result = self.query_experiment_components([SBOLConstants.NCIT_STRAIN, SBOLConstants.OBI_STRAIN], collections, comp_labels[0], comp_labels[1:], trace_derivation, all_types=False, experiments=experiments)

		if pretty:
			if by_sample:
				return self.format_query_result(query_result, comp_labels[:-1], comp_labels[-1])
			else:
				return self.format_query_result(query_result, comp_labels)
		else:
			return query_result

	# Retrieves the URIs for all strains used in the specified collection of experiments.
	# This collection is typically associated with a challenge problem.
	def query_experiment_set_strains(self, collection, verbose=False, trace_derivation=True, by_sample=False, pretty=True):
		return self.query_experiment_strains(verbose, trace_derivation, by_sample, pretty, [collection])

	# Retrieves the URIs for all inducers in the specified experiment.
	def query_single_experiment_strains(self, experiment, verbose=False, trace_derivation=True, by_sample=True, pretty=True):
		return self.query_experiment_strains(verbose, trace_derivation, by_sample, pretty, experiments=[experiment])

	# Sample query methods \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

	def query_single_experiment_samples_by_probability(self, experiment, threshold):
		sample_query = """
		PREFIX sd2: <http://sd2e.org#> 
		PREFIX prov: <http://www.w3.org/ns/prov#> 
		SELECT ?sample ?prob WHERE {{ 
  			<{exp}> sd2:experimentalData ?data;
  				sd2:matches_sample ?intent_sample .
  			?data prov:wasDerivedFrom+ ?sample .
  			?intent_sample sd2:has_sample ?sample .
  			?intent_sample sd2:has_probability ?prob
  			FILTER (?prob <= {thr})
		}}
		""".format(exp=experiment, thr=threshold)

		return self.fetch_SPARQL(self._server, sample_query)

	# Experiment data query methods \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

	# Retrieves the source URLs for all experimental data files generated by the specified experiment and their associated samples.
	def query_single_experiment_data(self, experiment, pretty=True):
		exp_data_query = """
		PREFIX sd2: <http://sd2e.org#>
		PREFIX prov: <http://www.w3.org/ns/prov#> 
		SELECT DISTINCT ?sample ?source WHERE {{ 
  			<{exp}> sd2:experimentalData ?data .
  			?data prov:wasDerivedFrom ?sample;
  				sd2:attachment ?attach .
  			?attach sd2:source ?source
		}}
		""".format(exp=experiment)

		exp_data_query_result = self.fetch_SPARQL(self._server, exp_data_query)

		if pretty:
			return self.format_query_result(exp_data_query_result, ['source'], 'sample')
		else:
			return exp_data_query_result

	# Experiment intent query methods \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

	# Retrieves the experimental intent JSON for the specified experiment.
	def query_single_experiment_intent(self, experiment):
		intent_query = """
		PREFIX sd2: <http://sd2e.org#>
		PREFIX dcterms: <http://purl.org/dc/terms/>
		SELECT ?dname ?ename ?oname ?ddef ?edef ?odef
		WHERE {{ {{
  			<{exp}> sd2:experimentalDesign ?design .
  			?design sd2:diagnosticVariable ?dvar .
  			?dvar dcterms:title ?dname .
  			OPTIONAL {{?dvar sd2:definition ?ddef}}
  		}} UNION {{
  			<{exp}> sd2:experimentalDesign ?design .
  			?design sd2:experimentalVariable ?evar .
  			?evar dcterms:title ?ename .
  			OPTIONAL {{?evar sd2:definition ?edef}}
  		}} UNION {{
  			<{exp}> sd2:experimentalDesign ?design .
  			?design sd2:outcomeVariable ?ovar .
  			?ovar dcterms:title ?oname .
  			OPTIONAL {{?ovar sd2:definition ?odef}}
  		}} }}
		""".format(exp=experiment)

		intent_data = self.fetch_SPARQL(self._server, intent_query)

		exp_intent = {'diagnostic-variables': [], 'experimental-variables': [], 'outcome-variables': [], 'truth-table': {'input': [], 'output': []}}

		level_switcher = {}

		for binding in intent_data['results']['bindings']:
			try:
				try:
					intent['diagnostic-variables'].append({'name': binding['dname']['value'], 'uri': binding['ddef']['value']})
				except:
					intent['diagnostic-variables'].append({'name': binding['dname']['value']})
			except:
				try:
					try:
						exp_intent['outcome-variables'].append({'name': binding['oname']['value'], 'uri': binding['odef']['value']})
					except:
						exp_intent['outcome-variables'].append({'name': binding['oname']['value']})
				except:
					ename = binding['ename']['value']
					try:
						assert ename in level_switcher
					except:
						level_switcher[ename] = len(exp_intent['experimental-variables'])
						try:
							exp_intent['experimental-variables'].append({'name': ename, 'uri': binding['edef']['value']})
						except:
							exp_intent['experimental-variables'].append({'name': ename})
					
		truth_table_query = """
		PREFIX sd2: <http://sd2e.org#>
		PREFIX dcterms: <http://purl.org/dc/terms/>
		SELECT ?defin ?emag ?ename ?omag ?oname
		WHERE {{ {{
  			<{exp}> sd2:experimentalDesign ?design .
  			?design sd2:experimentalCondition ?cond .
  			?cond sd2:definition ?defin ;
  				sd2:experimentalLevel ?elevel .
  			?elevel sd2:level ?emag ;
  				sd2:experimentalVariable ?evar .
  			?evar dcterms:title ?ename
		}} UNION {{
			<{exp}> sd2:experimentalDesign ?design .
  			?design sd2:experimentalCondition ?cond .
  			?cond sd2:definition ?defin ;
  				sd2:outcomeLevel ?olevel .
  			?olevel sd2:level ?omag ;
  				sd2:experimentalVariable ?ovar .
  			?ovar dcterms:title ?oname
		}} }}
		""".format(exp=experiment)

		truth_table_data = self.fetch_SPARQL(self._server, truth_table_query)

		input_switcher = {}

		for binding in truth_table_data['results']['bindings']:
			defin = binding['defin']['value']
			try:
				assert defin in input_switcher
			except:
				input_switcher[defin] = len(exp_intent['truth-table']['input'])
				exp_intent['truth-table']['input'].append({'experimental-variables': [], 'strain': defin})

		for tt_input in exp_intent['truth-table']['input']:
			exp_intent['truth-table']['output'].append('-')
			for evar in exp_intent['experimental-variables']:
				tt_input['experimental-variables'].append('-')

		for binding in truth_table_data['results']['bindings']:
			i = input_switcher[binding['defin']['value']]
			tt_input = exp_intent['truth-table']['input'][i]
			try:
				j = level_switcher[binding['ename']['value']]
				tt_input['experimental-variables'][j] = int(binding['emag']['value'])
			except:
				exp_intent['truth-table']['output'][i] = int(binding['omag']['value'])

		return json.dumps(exp_intent, separators=(',',':'))

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

		return self.fetch_SPARQL(self._server, design_set_query)

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

		return self.fetch_SPARQL(self._server, exp_set_query)

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

		return self.fetch_SPARQL(self._server, exp_set_size_query)

	def query_synbiohub_statistics(self):
		design_riboswitches = repr(len(self.query_design_riboswitches(pretty=True)))
		exp_riboswitches = repr(len(self.query_experiment_riboswitches(by_sample=False)))

		print(exp_riboswitches + ' out of ' + design_riboswitches + ' riboswitches')

		design_plasmids = repr(len(self.query_design_plasmids(pretty=True)))
		exp_plasmids = repr(len(self.query_experiment_plasmids(by_sample=False)))

		print(exp_plasmids + ' out of ' + design_plasmids + ' plasmids')

		design_gates = repr(len(self.query_design_gates(pretty=True)))
		exp_gates = repr(len(self.query_experiment_gates(by_sample=False)))

		print(exp_gates + ' out of ' + design_gates + ' gates')

		design_media = repr(len(self.query_design_media(pretty=True)))
		exp_media = repr(len(self.query_experiment_media(by_sample=False)))

		print(exp_media + ' out of ' + design_media + ' media')

		design_controls= repr(len(self.query_design_controls(pretty=True)))
		exp_controls= repr(len(self.query_experiment_controls(by_sample=False)))

		print(exp_controls + ' out of ' + design_controls + ' controls')

		exp_query_result = self.query_collection_members(collections=[SD2Constants.SD2_EXPERIMENT_COLLECTION], rdf_type='http://sd2e.org#Experiment')

		print(repr(len(self.format_query_result(exp_query_result, ['entity']))) + ' experiment plans')

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
		sbh_connector = login_SBH(self._server)
		self.submit_Collection(sbh_connector, sbolDoc, True, 0)

	# Submit the given SBOL Document to an existing SynBioHub Collection
	# sbolDoc: The SBOL Document that the user wants to submit to the existing SynBioHub Collection
	# collURI: The URI of the SynBioHub Collection that the user would like to submit to
	# ovewrite: An integer variable to indicate whether the data submitting to the existing SynBioHub collection should override information.
	# 	Note: Setting the variable overwrite = 1 (ovewrite existing collection data) or 2 (merge existing collection data with new data). 0 will be set as default.
	def submit_ExistingCollection(self, sbolDoc, collURI, overwrite):
		sbolDoc.identity = collURI
		sbh_connector = login_SBH(self._server)
		self.submit_Collection(sbh_connector, sbolDoc, False, overwrite)
