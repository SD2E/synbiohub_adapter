import unittest

from query_synbiohub import *

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

	def test_query(self):
		server = "http://hub-api.sd2e.org:80/sparql"
		collection = '<http://hub.sd2e.org/user/nicholasroehner/rule_30/rule_30_collection/1>'

		sbhQuery = query_synbiohub(server)
		sample = sbhQuery.query_Sample(collection)
		print(sample)

if __name__ == '__main__':
	unittest.main()