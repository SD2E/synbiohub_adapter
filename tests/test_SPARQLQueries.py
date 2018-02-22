import unittest

from query_synbiohub import *
from SynBioHubUtil import SBHConstants 

class TestSBHQueries(unittest.TestCase):
	'''
		This class will perform unit testing to query information from SynBioHub SD2 instance. 

		Installation Requirement(s):
		- This test environment will need SPARQLWrapper installed to run successfully. 
			SPARQLWrapper is used to remotely execute SynBioHub queries.

		To run this python file, enter in the following command from the synbiohub_adapter directory:
			python -m unittest tests/test_SPARQLQueries.py
	'''

	def setup_test1(self):
		self.assertEqual(True)

	def test_query_challenge_inducers(self):
		rule_30_collection = SBHConstants.RULE_30_COLLECTION
		
		sbh_query = SynBioHubQuery(SBHConstants.SD2_SERVER)
		inducers = sbh_query.query_challenge_inducers(rule_30_collection)
		print(inducers)

	def test_query_challenge_plasmids(self):
		rule_30_collection = SBHConstants.RULE_30_COLLECTION

		sbh_query = SynBioHubQuery(SBHConstants.SD2_SERVER)
		plasmids = sbh_query.query_challenge_plasmids(rule_30_collection)
		print(plasmids)

	def test_query_experiment_inducers(self):
		rule_30_experiment = '<https://hub.sd2e.org/user/sd2e/rule_30/transcriptic_rule_30_q0_1_09242017/1>'

		sbh_query = SynBioHubQuery(SBHConstants.SD2_SERVER)
		inducer = sbh_query.query_experiment_inducers(experiment)
		print(inducer)

	def test_query_experiment_plasmids(self):
		rule_30_experiment = '<https://hub.sd2e.org/user/sd2e/rule_30/transcriptic_rule_30_q0_1_09242017/1>'

		sbh_query = SynBioHubQuery(SBHConstants.SD2_SERVER)
		inducer = sbh_query.query_experiment_plasmids(rule_30_experiment)
		print(inducer)

	# def test_bbn_sbh(self):
	# 	server = SBHConstants.BBN_SERVER
	# 	collection = SBHConstants.BBN_YEASTGATES_COLLECTION
	# 	sbh_query = SynBioHubQuery(server)
	# 	sample = sbh_query.query_Sample(collection)

if __name__ == '__main__':
	unittest.main()