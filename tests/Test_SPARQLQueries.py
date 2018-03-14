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

	def test_query_design_inducers(self):
		sbh_query = SynBioHubQuery(SBHConstants.SD2_SERVER)
		inducers = sbh_query.query_design_inducers(SBHConstants.YEAST_GATES_DESIGN_COLLECTION)
		print(inducers)

	def test_query_design_plasmids(self):
		sbh_query = SynBioHubQuery(SBHConstants.SD2_SERVER)
		plasmids = sbh_query.query_design_plasmids(SBHConstants.YEAST_GATES_DESIGN_COLLECTION)
		print(plasmids)

	def test_query_design_strains(self):
		sbh_query = SynBioHubQuery(SBHConstants.SD2_SERVER)
		strains = sbh_query.query_design_strains(SBHConstants.YEAST_GATES_DESIGN_COLLECTION)
		print(strains)

	def test_query_experiment_sets(self):
		sbh_query = SynBioHubQuery(SBHConstants.SD2_SERVER)
		exp_sets = sbh_query.query_experiment_sets()
		print(exp_sets)

	def test_query_experiment_set_count(self):
		sbh_query = SynBioHubQuery(SBHConstants.SD2_SERVER)
		exp_count = sbh_query.query_experiment_set_count(SBHConstants.RULE_30_EXPERIMENT_COLLECTION)
		print(exp_count)

	def test_query_experiment_set_inducers(self):
		sbh_query = SynBioHubQuery(SBHConstants.SD2_SERVER)
		inducers = sbh_query.query_experiment_set_inducers(SBHConstants.RULE_30_EXPERIMENT_COLLECTION)
		print(inducers)

	def test_query_experiment_set_plasmids(self):
		sbh_query = SynBioHubQuery(SBHConstants.SD2_SERVER)
		plasmids = sbh_query.query_experiment_set_plasmids(SBHConstants.RULE_30_EXPERIMENT_COLLECTION)
		print(plasmids)

	def test_query_experiment_set_strains(self):
		sbh_query = SynBioHubQuery(SBHConstants.SD2_SERVER)
		strains = sbh_query.query_experiment_set_strains(SBHConstants.RULE_30_EXPERIMENT_COLLECTION)
		print(strains)

	def test_query_experiment_inducers(self):
		rule_30_experiment = '<https://hub.sd2e.org/user/sd2e/experiment/transcriptic_rule_30_q0_1_09242017/1>'

		sbh_query = SynBioHubQuery(SBHConstants.SD2_SERVER)
		inducers = sbh_query.query_experiment_inducers(rule_30_experiment)
		print(inducers)

	def test_query_experiment_plasmids(self):
		rule_30_experiment = '<https://hub.sd2e.org/user/sd2e/experiment/transcriptic_rule_30_q0_1_09242017/1>'

		sbh_query = SynBioHubQuery(SBHConstants.SD2_SERVER)
		plasmids = sbh_query.query_experiment_plasmids(rule_30_experiment)
		print(plasmids)

	def test_query_experiment_strains(self):
		rule_30_experiment = '<https://hub.sd2e.org/user/sd2e/experiment/transcriptic_rule_30_q0_1_09242017/1>'

		sbh_query = SynBioHubQuery(SBHConstants.SD2_SERVER)
		strains = sbh_query.query_experiment_strains(rule_30_experiment)
		print(strains)

	def test_query_experiment_data(self):
		rule_30_experiment = '<https://hub.sd2e.org/user/sd2e/experiment/transcriptic_rule_30_q0_1_09242017/1>'

		sbh_query = SynBioHubQuery(SBHConstants.SD2_SERVER)
		exp_data = sbh_query.query_experiment_data(rule_30_experiment)
		print(exp_data)

	# Note: This BBN instance will successfully query infomration if the user is directly connected to BBN's server
	# def test_bbnSBH(self):
	# 	server = SBHConstants.BBN_SERVER
	# 	collection = SBHConstants.BBN_RULE30_COLLECTION
	# 	sbhQuery = SynBioHubQuery(server)
	# 	sample = sbhQuery.query_experiment_plasmids(collection)
	# 	print('Successfully Queried BBN instance!')


if __name__ == '__main__':
	unittest.main()