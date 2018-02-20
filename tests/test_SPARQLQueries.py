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

	def test_inducerQuery(self):
		server = SBHConstants.SD2_SERVER
		collection = SBHConstants.RULE30_COLLECTION

		sbhQuery = SynbiohubQuery(server)
		inducer = sbhQuery.query_Inducer(collection)
		print(inducer)

	def test_plasmidQuery(self):
		server = SBHConstants.SD2_SERVER
		collection = SBHConstants.RULE30_COLLECTION

		sbhQuery = SynbiohubQuery(server)
		plasmid = sbhQuery.query_Plasmid(collection)
		print(plasmid)

	def test_sampleQuery(self):
		server = SBHConstants.SD2_SERVER
		collection = SBHConstants.RULE30_COLLECTION

		sbhQuery = SynbiohubQuery(server)
		sample = sbhQuery.query_Sample(collection)
		# print(sample)

	def test_bbnSBH(self):
		server = SBHConstants.BBN_SERVER
		collection = SBHConstants.BBN_YEASTGATES_COLLECTION
		sbhQuery = SynbiohubQuery(server)
		sample = sbhQuery.query_Sample(collection)

if __name__ == '__main__':
	unittest.main()