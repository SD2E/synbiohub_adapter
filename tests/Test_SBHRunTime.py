import timeit

from synbiohub_adapter.query_synbiohub import *
from synbiohub_adapter.SynBioHubUtil import *
from sbol import *

'''
	This module is used to calculate the run time when pushing and pulling datt to and from SynBioHub.
	Information about the run time is outputted into a CSV file.

	To run this python module, enter in the following command from the synbiohub_adapter directory:
		python -m tests.Test_SBHRunTime

	author(s) : Tramy Nguyen
'''
def push_sbh():
	print("hello")

if __name__ == '__main__':
	sbolDoc = loadSBOLFile('examples/rule30-Q0-v2.xml')
	sbhQuery = SynBioHubQuery(SBHConstants.BBN_SERVER)
	sbh_connector = sbhQuery.login_SBH()

