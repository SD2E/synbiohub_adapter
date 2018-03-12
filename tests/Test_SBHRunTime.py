
import time

from synbiohub_adapter.query_synbiohub import *
from synbiohub_adapter.SynBioHubUtil import *
from sbol import *

'''
	This module is used to calculate the run time when pushing and pulling data to and from SynBioHub.
	Information about the run time is outputted into a CSV file.

	To run this python module, enter in the following command from the synbiohub_adapter directory:
		python -m tests.Test_SBHRunTime

	author(s) : Tramy Nguyen
'''

# Returns the time (seconds) it takes to make a push to a new Collection on SynBioHub
def push_sbh(sbolDoc, sbh_connector):
	start = time.clock()
	result = sbh_connector.submit(sbolDoc)
	end = time.clock()
	print(result)
	if result != 'Successfully uploaded':
		sys.exit()
	return end - start

# Returns the time (seconds) it takes to make a pull from an existing SynBioHub Collection
def pull_sbh(sbh_connector, sbolURI):
	sbolDoc = Document()
	start = time.clock()
	sbh_connector.pull(sbolURI, sbolDoc)
	end = time.clock()
	return end - start 

# Calculates the speed (seconds) to push and pull data to/from SynBioHub
# number: The number of pushes to SynBioHub
def testSpeed(number):
	sbolFile = 'examples/rule30-Q0-v2.xml'
	sbolDoc = Document()
	sbolDoc.read(sbolFile)

	sbh_connector = PartShop("https://synbiohub.bbn.com/")
	sbh_user = 'tramy.t.nguyen@raytheon.com'
	sbh_connector.login(sbh_user, getpass.getpass(prompt='Enter SynBioHub Password: ', stream=sys.stderr))

	total_pushTime = total_pullTime = 0
	mult = 2 
	for i in range(number):
		sbolDoc.displayId = "TestColl_" + str(i)
		sbolDoc.name = "TestColl_" + str(i) + "_name"
		sbolDoc.version = str(i)
		sbolDoc.description = "TestColl_" + str(i) + "_description"
		total_pushTime += push_sbh(sbolDoc, sbh_connector)
		
		if i % mult == 0:
			uri = "http://hub.sd2e.org/user/sd2e/transcriptic_rule_30_q0_1_09242017/transform_pAN1201_NEB_10_beta_to_NEB_10_beta_pAN1201/1.0.0"
			total_pullTime += pull_sbh(sbh_connector, uri)
		
	print("Total time for push: %f seconds" % total_pushTime) 
	print("Total time for pull: %f seconds" % total_pullTime) 

# Calculate how many pull and push were made to SynBioHub for a specified time
# totalTime: How long to push and pull from SynBioHub
def testThroughput(totalTime):
	sbolFile = 'examples/rule30-Q0-v2.xml'
	sbolDoc = Document()
	sbolDoc.read(sbolFile)

	sbh_connector = PartShop("https://synbiohub.bbn.com/")
	sbh_user = 'tramy.t.nguyen@raytheon.com'
	sbh_connector.login(sbh_user, getpass.getpass(prompt='Enter SynBioHub Password: ', stream=sys.stderr))

	startTime = time.clock()

	numPush = 0
	while time.clock() - startTime < totalTime:
		sbolDoc.displayId = "ThroughputTest_Coll_" + str(numPush)
		sbolDoc.name = "ThroughputTest_Coll_" + str(numPush) + "_name"
		sbolDoc.version = str(numPush)
		sbolDoc.description = "ThroughputTest_Coll_" + str(numPush) + "_description"
		
		push_sbh(sbolDoc, sbh_connector)
		numPush += 1

	print("%d pushes in %d seconds" % (numPush, totalTime))

if __name__ == '__main__':
	# testSpeed(3)
	# testThroughput(30) # number of seconds