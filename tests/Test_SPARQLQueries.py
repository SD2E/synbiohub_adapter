import unittest

from synbiohub_adapter.query_synbiohub import *
from synbiohub_adapter.SynBioHubUtil import *
from sbol import *

class TestSBHQueries(unittest.TestCase):
	'''
		This class will perform unit testing to query information from SynBioHub's instances. 

		Installation Requirement(s):
		- This test environment will need SPARQLWrapper installed to run successfully. 
			SPARQLWrapper is used to remotely execute SynBioHub queries.

		To run this python file, enter in the following command from the synbiohub_adapter directory:
			python -m unittest tests/Test_SPARQLQueries.py

		author(s) : Nicholas Roehner
					Tramy Nguyen
	'''

	# Test collection query methods \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

	def test_query_collection_members(self):
		sbh_query = SynBioHubQuery(SD2Constants.SD2_SERVER)
		members = sbh_query.query_collection_members([SD2Constants.YEAST_GATES_DESIGN_COLLECTION], ['https://hub.sd2e.org/user/sd2e/design/UWBF_7376/1', 'https://hub.sd2e.org/user/sd2e/design/pAN4036/1'])
		print(members)

	# Test control query methods \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

	def test_query_design_controls(self):
		sbh_query = SynBioHubQuery(SD2Constants.SD2_SERVER)
		controls = sbh_query.query_design_controls()
		print(controls)

	def test_query_design_set_controls(self):
		sbh_query = SynBioHubQuery(SD2Constants.SD2_SERVER)
		controls = sbh_query.query_design_set_controls(SD2Constants.YEAST_GATES_DESIGN_COLLECTION)
		print(controls)

	def test_query_design_fbead_controls(self):
		sbh_query = SynBioHubQuery(SD2Constants.SD2_SERVER)
		controls = sbh_query.query_design_fbead_controls()
		print(controls)

	def test_query_design_set_fbead_controls(self):
		sbh_query = SynBioHubQuery(SD2Constants.SD2_SERVER)
		controls = sbh_query.query_design_set_fbead_controls(SD2Constants.YEAST_GATES_DESIGN_COLLECTION)
		print(controls)

	def test_query_design_fluorescein_controls(self):
		sbh_query = SynBioHubQuery(SD2Constants.SD2_SERVER)
		controls = sbh_query.query_design_fluorescein_controls()
		print(controls)

	def test_query_design_set_fluorescein_controls(self):
		sbh_query = SynBioHubQuery(SD2Constants.SD2_SERVER)
		controls = sbh_query.query_design_set_fluorescein_controls(SD2Constants.YEAST_GATES_DESIGN_COLLECTION)
		print(controls)

	def test_query_design_ludox_controls(self):
		sbh_query = SynBioHubQuery(SD2Constants.SD2_SERVER)
		controls = sbh_query.query_design_ludox_controls()
		print(controls)

	def test_query_design_set_ludox_controls(self):
		sbh_query = SynBioHubQuery(SD2Constants.SD2_SERVER)
		controls = sbh_query.query_design_set_ludox_controls(SD2Constants.YEAST_GATES_DESIGN_COLLECTION)
		print(controls)

	def test_query_design_water_controls(self):
		sbh_query = SynBioHubQuery(SD2Constants.SD2_SERVER)
		controls = sbh_query.query_design_water_controls()
		print(controls)

	def test_query_design_set_water_controls(self):
		sbh_query = SynBioHubQuery(SD2Constants.SD2_SERVER)
		controls = sbh_query.query_design_set_water_controls(SD2Constants.YEAST_GATES_DESIGN_COLLECTION)
		print(controls)

	def test_query_experiment_controls(self):
		sbh_query = SynBioHubQuery(SD2Constants.SD2_SERVER)
		controls = sbh_query.query_experiment_controls()
		print(controls)

	def test_query_experiment_set_controls(self):
		sbh_query = SynBioHubQuery(SD2Constants.SD2_SERVER)
		controls = sbh_query.query_experiment_set_controls(SD2Constants.YEAST_GATES_EXPERIMENT_COLLECTION)
		print(controls)

	def test_query_single_experiment_controls(self):
		yeast_gates_experiment = 'https://hub.sd2e.org/user/sd2e/experiment/transcriptic_yeast_gates_q0_r1bfbfd7f8dn5/1'

		sbh_query = SynBioHubQuery(SD2Constants.SD2_SERVER)
		controls = sbh_query.query_single_experiment_controls(yeast_gates_experiment)
		print(controls)

	def test_query_experiment_fbead_controls(self):
		sbh_query = SynBioHubQuery(SD2Constants.SD2_SERVER)
		controls = sbh_query.query_experiment_fbead_controls()
		print(controls)

	def test_query_experiment_set_fbead_controls(self):
		sbh_query = SynBioHubQuery(SD2Constants.SD2_SERVER)
		controls = sbh_query.query_experiment_set_fbead_controls(SD2Constants.YEAST_GATES_EXPERIMENT_COLLECTION)
		print(controls)

	def test_query_single_experiment_fbead_controls(self):
		yeast_gates_experiment = 'https://hub.sd2e.org/user/sd2e/experiment/transcriptic_yeast_gates_q0_r1bfbfd7f8dn5/1'

		sbh_query = SynBioHubQuery(SD2Constants.SD2_SERVER)
		controls = sbh_query.query_single_experiment_fbead_controls(yeast_gates_experiment)
		print(controls)

	def test_query_experiment_fluorescein_controls(self):
		sbh_query = SynBioHubQuery(SD2Constants.SD2_SERVER)
		controls = sbh_query.query_experiment_fluorescein_controls()
		print(controls)

	def test_query_experiment_set_fluorescein_controls(self):
		sbh_query = SynBioHubQuery(SD2Constants.SD2_SERVER)
		controls = sbh_query.query_experiment_set_fluorescein_controls(SD2Constants.YEAST_GATES_EXPERIMENT_COLLECTION)
		print(controls)

	def test_query_single_experiment_fluorescein_controls(self):
		yeast_gates_experiment = 'https://hub.sd2e.org/user/sd2e/experiment/transcriptic_yeast_gates_q0_r1bfbfd7f8dn5/1'

		sbh_query = SynBioHubQuery(SD2Constants.SD2_SERVER)
		controls = sbh_query.query_single_experiment_fluorescein_controls(yeast_gates_experiment)
		print(controls)

	def test_query_experiment_ludox_controls(self):
		sbh_query = SynBioHubQuery(SD2Constants.SD2_SERVER)
		controls = sbh_query.query_experiment_ludox_controls()
		print(controls)

	def test_query_experiment_set_ludox_controls(self):
		sbh_query = SynBioHubQuery(SD2Constants.SD2_SERVER)
		controls = sbh_query.query_experiment_set_ludox_controls(SD2Constants.YEAST_GATES_EXPERIMENT_COLLECTION)
		print(controls)

	def test_query_single_experiment_ludox_controls(self):
		yeast_gates_experiment = 'https://hub.sd2e.org/user/sd2e/experiment/transcriptic_yeast_gates_q0_r1bfbfd7f8dn5/1'

		sbh_query = SynBioHubQuery(SD2Constants.SD2_SERVER)
		controls = sbh_query.query_single_experiment_ludox_controls(yeast_gates_experiment)
		print(controls)

	def test_query_experiment_water_controls(self):
		sbh_query = SynBioHubQuery(SD2Constants.SD2_SERVER)
		controls = sbh_query.query_experiment_water_controls()
		print(controls)

	def test_query_experiment_set_water_controls(self):
		sbh_query = SynBioHubQuery(SD2Constants.SD2_SERVER)
		controls = sbh_query.query_experiment_set_water_controls(SD2Constants.YEAST_GATES_EXPERIMENT_COLLECTION)
		print(controls)	

	def test_query_single_experiment_water_controls(self):
		yeast_gates_experiment = 'https://hub.sd2e.org/user/sd2e/experiment/transcriptic_yeast_gates_q0_r1bfbfd7f8dn5/1'

		sbh_query = SynBioHubQuery(SD2Constants.SD2_SERVER)
		controls = sbh_query.query_single_experiment_water_controls(yeast_gates_experiment)
		print(controls)	

	# Test gate query methods \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

	def test_query_design_gates(self):
		sbh_query = SynBioHubQuery(SD2Constants.SD2_SERVER)
		gates = sbh_query.query_design_gates()
		print(gates)

	def test_query_design_set_gates(self):
		sbh_query = SynBioHubQuery(SD2Constants.SD2_SERVER)
		gates = sbh_query.query_design_set_gates(SD2Constants.YEAST_GATES_DESIGN_COLLECTION)
		print(gates)

	def test_query_experiment_gates(self):
		sbh_query = SynBioHubQuery(SD2Constants.SD2_SERVER)
		gates = sbh_query.query_experiment_gates()
		print(gates)

	def test_query_experiment_set_gates(self):
		sbh_query = SynBioHubQuery(SD2Constants.SD2_SERVER)
		gates = sbh_query.query_experiment_set_gates(SD2Constants.YEAST_GATES_EXPERIMENT_COLLECTION)
		print(gates)

	def test_query_single_experiment_gates(self):
		yeast_gates_experiment = 'https://hub.sd2e.org/user/sd2e/experiment/biofab_yeast_gates_q0_aq_11269_4/1'

		sbh_query = SynBioHubQuery(SD2Constants.SD2_SERVER)
		gates = sbh_query.query_single_experiment_gates(yeast_gates_experiment)
		print(gates)

	# Test inducer query methods \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

	def test_query_design_set_inducers(self):
		sbh_query = SynBioHubQuery(SD2Constants.SD2_SERVER)
		inducers = sbh_query.query_design_set_inducers(SD2Constants.RULE_30_DESIGN_COLLECTION)
		print(inducers)

	def test_query_design_inducers(self):
		sbh_query = SynBioHubQuery(SD2Constants.SD2_SERVER)
		inducers = sbh_query.query_design_inducers()
		print(inducers)

	def test_query_single_experiment_inducers(self):
		rule_30_experiment = 'https://hub.sd2e.org/user/sd2e/experiment/transcriptic_rule_30_q0_1_09242017/1'

		sbh_query = SynBioHubQuery(SD2Constants.SD2_SERVER)
		inducers = sbh_query.query_single_experiment_inducers(rule_30_experiment)
		print(inducers)

	def test_query_experiment_set_inducers(self):
		sbh_query = SynBioHubQuery(SD2Constants.SD2_SERVER)
		inducers = sbh_query.query_experiment_set_inducers(SD2Constants.RULE_30_EXPERIMENT_COLLECTION)
		print(inducers)

	def test_query_experiment_inducers(self):
		sbh_query = SynBioHubQuery(SD2Constants.SD2_SERVER)
		inducers = sbh_query.query_experiment_inducers()
		print(inducers)

	def test_query_sample_inducers(self):
		rule_30_sample = 'https://hub.sd2e.org/user/sd2e/transcriptic_rule_30_q0_1_09242017/H07/1'

		sbh_query = SynBioHubQuery(SD2Constants.SD2_SERVER)
		inducers = sbh_query.query_sample_inducers(rule_30_sample)
		print(inducers)

	def test_query_condition_inducers(self):
		rule_30_condition = 'https://hub.sd2e.org/user/sd2e/transcriptic_rule_30_q0_1_09242017/NEB_10_beta_pAN1717_Larabinose_5_aTc_0p002_IPTG_1_system/1'

		sbh_query = SynBioHubQuery(SD2Constants.SD2_SERVER)
		inducers = sbh_query.query_condition_inducers(rule_30_condition)
		print(inducers)

	# Test media query methods \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

	def test_query_design_set_media(self):
		sbh_query = SynBioHubQuery(SD2Constants.SD2_SERVER)
		media = sbh_query.query_design_set_media(SD2Constants.YEAST_GATES_DESIGN_COLLECTION)
		print(media)

	def test_query_design_media(self):
		sbh_query = SynBioHubQuery(SD2Constants.SD2_SERVER)
		media = sbh_query.query_design_media()
		print(media)

	def test_query_experiment_media(self):
		sbh_query = SynBioHubQuery(SD2Constants.SD2_SERVER)
		media = sbh_query.query_experiment_media()
		print(media)

	def test_query_experiment_set_media(self):
		sbh_query = SynBioHubQuery(SD2Constants.SD2_SERVER)
		media = sbh_query.query_experiment_set_media(SD2Constants.YEAST_GATES_EXPERIMENT_COLLECTION)
		print(media)

	def test_query_single_experiment_media(self):
		yeast_gates_experiment = 'https://hub.sd2e.org/user/sd2e/experiment/biofab_yeast_gates_q0_aq_11269_4/1'

		sbh_query = SynBioHubQuery(SD2Constants.SD2_SERVER)
		media = sbh_query.query_single_experiment_media(yeast_gates_experiment)
		print(media)

	# Test plasmid query methods \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

	def test_query_design_plasmids(self):
		sbh_query = SynBioHubQuery(SD2Constants.SD2_SERVER)
		plasmids = sbh_query.query_design_plasmids()
		print(plasmids)

	def test_query_design_set_plasmids(self):
		sbh_query = SynBioHubQuery(SD2Constants.SD2_SERVER)
		plasmids = sbh_query.query_design_set_plasmids(SD2Constants.YEAST_GATES_DESIGN_COLLECTION)
		print(plasmids)

	def test_query_experiment_plasmids(self):
		sbh_query = SynBioHubQuery(SD2Constants.SD2_SERVER)
		plasmids = sbh_query.query_experiment_plasmids()
		print(plasmids)

	def test_query_experiment_set_plasmids(self):
		sbh_query = SynBioHubQuery(SD2Constants.SD2_SERVER)
		plasmids = sbh_query.query_experiment_set_plasmids(SD2Constants.RULE_30_EXPERIMENT_COLLECTION)
		print(plasmids)

	def test_query_single_experiment_plasmids(self):
		yeast_gates_experiment = 'https://hub.sd2e.org/user/sd2e/experiment/biofab_yeast_gates_q0_aq_11269_4/1'

		sbh_query = SynBioHubQuery(SD2Constants.SD2_SERVER)
		plasmids = sbh_query.query_single_experiment_plasmids(yeast_gates_experiment)
		print(plasmids)

	def test_query_sample_plasmids(self):
		rule_30_sample = 'https://hub.sd2e.org/user/sd2e/transcriptic_rule_30_q0_1_09242017/H07/1'

		sbh_query = SynBioHubQuery(SD2Constants.SD2_SERVER)
		plasmids = sbh_query.query_sample_plasmids(rule_30_sample)
		print(plasmids)

	def test_query_condition_plasmids(self):
		rule_30_condition = 'https://hub.sd2e.org/user/sd2e/transcriptic_rule_30_q0_1_09242017/NEB_10_beta_pAN1717_Larabinose_5_aTc_0p002_IPTG_1_system/1'

		sbh_query = SynBioHubQuery(SD2Constants.SD2_SERVER)
		plasmids = sbh_query.query_condition_plasmids(rule_30_condition)
		print(plasmids)

	# Test riboswitch query methods \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

	def test_query_design_riboswitches(self):
		sbh_query = SynBioHubQuery(SD2Constants.SD2_SERVER)
		riboswitches = sbh_query.query_design_riboswitches()
		print(riboswitches)

	def test_query_design_set_riboswitches(self):
		sbh_query = SynBioHubQuery(SD2Constants.SD2_SERVER)
		riboswitches = sbh_query.query_design_set_riboswitches(SD2Constants.RIBOSWITCHES_DESIGN_COLLECTION)
		print(riboswitches)

	def test_query_experiment_riboswitches(self):
		sbh_query = SynBioHubQuery(SD2Constants.SD2_SERVER)
		riboswitches = sbh_query.query_experiment_riboswitches()
		print(riboswitches)

	# Test strain query methods \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

	def test_query_design_strains(self):
		sbh_query = SynBioHubQuery(SD2Constants.SD2_SERVER)
		strains = sbh_query.query_design_strains()
		print(strains)

	def test_query_design_set_strains(self):
		sbh_query = SynBioHubQuery(SD2Constants.SD2_SERVER)
		strains = sbh_query.query_design_set_strains(SD2Constants.YEAST_GATES_DESIGN_COLLECTION)
		print(strains)

	def test_query_experiment_strains(self):
		sbh_query = SynBioHubQuery(SD2Constants.SD2_SERVER)
		strains = sbh_query.query_experiment_strains()
		print(strains)

	def test_query_experiment_set_strains(self):
		sbh_query = SynBioHubQuery(SD2Constants.SD2_SERVER)
		strains = sbh_query.query_experiment_set_strains(SD2Constants.RULE_30_EXPERIMENT_COLLECTION)
		print(strains)

	def test_query_single_experiment_strains(self):
		rule_30_experiment = 'https://hub.sd2e.org/user/sd2e/experiment/transcriptic_rule_30_q0_1_09242017/1'

		sbh_query = SynBioHubQuery(SD2Constants.SD2_SERVER)
		strains = sbh_query.query_single_experiment_strains(rule_30_experiment)
		print(strains)

	# Test sample query methods \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

	def test_query_single_experiment_samples_by_probability(self):
		yeast_gates_experiment = 'https://hub.sd2e.org/user/sd2e/experiment/biofab_yeast_gates_q0_aq_10843/1'

		sbh_query = SynBioHubQuery(SD2Constants.SD2_SERVER)
		samples = sbh_query.query_single_experiment_samples_by_probability(yeast_gates_experiment, 0.4)
		print(samples)

	# Test experiment data query methods \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

	def test_query_single_experiment_data(self):
		yeast_gates_experiment = 'https://hub.sd2e.org/user/sd2e/experiment/biofab_yeast_gates_q0_aq_10843/1'

		sbh_query = SynBioHubQuery(SD2Constants.SD2_SERVER)
		exp_data = sbh_query.query_single_experiment_data(yeast_gates_experiment)
		print(exp_data)

	# Test experiment intent query methods \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

	def test_query_single_experiment_intent(self):
		yeast_gates_experiment = 'https://hub.sd2e.org/user/sd2e/experiment/biofab_yeast_gates_q0_aq_10843/1'

		sbh_query = SynBioHubQuery(SD2Constants.SD2_SERVER)
		exp_intent = sbh_query.query_single_experiment_intent(yeast_gates_experiment)
		print(exp_intent)

	# Test design and experiment set query methods \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

	def test_query_design_sets(self):
		sbh_query = SynBioHubQuery(SD2Constants.SD2_SERVER)
		design_sets = sbh_query.query_design_sets()
		print(design_sets)

	def test_query_experiment_sets(self):
		sbh_query = SynBioHubQuery(SD2Constants.SD2_SERVER)
		exp_sets = sbh_query.query_experiment_sets()
		print(exp_sets)

	def test_query_experiment_set_size(self):
		sbh_query = SynBioHubQuery(SD2Constants.SD2_SERVER)
		exp_set_size = sbh_query.query_experiment_set_size(SD2Constants.RULE_30_EXPERIMENT_COLLECTION)
		print(exp_set_size)

	# Test attachment retrieval methods \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

	def test_query_plan_attachments(self):
		sbh_query = SynBioHubQuery(SD2Constants.SD2_SERVER)
		plan_attachments = sbh_query.query_single_experiment_attachments("https://hub.sd2e.org/user/sd2e/experiment/biofab_yeast_gates_q0_aq_11269_1/1")
		assert plan_attachments is not None and len(plan_attachments['results']['bindings']) == 1
		print(plan_attachments)

		plan_attachments = sbh_query.query_single_experiment_attachments("foo")
		assert plan_attachments is not None and len(plan_attachments['results']['bindings']) == 0
		print(plan_attachments)

	def test_query_plan_named_attachments(self):
		sbh_query = SynBioHubQuery(SD2Constants.SD2_SERVER)
		plan_attachments = sbh_query.query_single_experiment_attachment("https://hub.sd2e.org/user/sd2e/experiment/biofab_yeast_gates_q0_intent_control_test/1", "biofab_yg_UWBF_NOR_intent_control_test.json")
		assert plan_attachments is not None and len(plan_attachments['results']['bindings']) == 1
		print(plan_attachments)

		plan_attachments = sbh_query.query_single_experiment_attachment("https://hub.sd2e.org/user/sd2e/experiment/biofab_yeast_gates_q0_intent_control_test/1", "biofab_yg_UWBF_NOR_intent_control_test_sample_attributes.json")
		assert plan_attachments is not None and len(plan_attachments['results']['bindings']) == 1
		print(plan_attachments)

		plan_attachments = sbh_query.query_single_experiment_attachment("https://hub.sd2e.org/user/sd2e/experiment/biofab_yeast_gates_q0_intent_control_test/1", "foo")
		assert plan_attachments is not None and len(plan_attachments['results']['bindings']) == 0
		print(plan_attachments)

	# Test statistics query methods \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

	# def test_query_synbiohub_statistics(self):
	# 	sbh_query = SynBioHubQuery(SD2Constants.SD2_SERVER)
	# 	sbh_query.query_synbiohub_statistics()

	# Note: This BBN instance will successfully query infomration if the user is directly connected to BBN's server
	# def test_bbnSBH(self):
	# 	server = SD2Constants.BBN_SERVER
	# 	collection = SD2Constants.BBN_RULE30_COLLECTION
	# 	sbhQuery = SynBioHubQuery(server)
	# 	sample = sbhQuery.query_experiment_plasmids(collection)
	# 	print('Successfully Queried BBN instance!')


if __name__ == '__main__':
	unittest.main()