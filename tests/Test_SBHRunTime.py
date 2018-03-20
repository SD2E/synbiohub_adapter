
import time
import pandas as pd
import matplotlib.pyplot as plt

from tests import myThread
from multiprocessing import Process, Queue
from multiprocessing import Pool

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
def testSpeed(iterations, sbolDoc, sbh_connector):
	pushTimes = []
	pullTimes = []

	for i in range(1,iterations):
		sbolDoc.displayId = "SpeedTestColl_" + str(i)
		sbolDoc.name = "SpeedTestColl_" + str(i) + "_name"
		sbolDoc.version = str(i)
		sbolDoc.description = "SpeedTestColl_" + str(i) + "_description"
		
		pushTime = push_sbh(sbolDoc, sbh_connector)
		pushTimes.append(pushTime)
	
		# pullTime = pull_sbh(sbh_connector, sbolDoc.displayId)
		pullTimes.append(0)
		
	return pullTimes, pushTimes

# Calculate how many pull and push were made to SynBioHub for a specified time
# totalTime: How long to push and pull from SynBioHub
def testSpeed2(totalTime, sbolDoc, sbh_connector):
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


# Returns a list of SBOLDocument generated from the rule30 example.
# numDocs: The number of SBOL documents this method should generate
# sbolFile: path to the sbol file that the SBOL document should be generated from
def create_sbolDocs(numDocs, sbolFile='examples/rule30-Q0-v2.xml'):
	doc_list = []
	for i in range(1,numDocs):
		sbolDoc = Document()
		sbolDoc.read(sbolFile)
		sbolDoc.displayId = "ThroughputTest_Coll_" + str(i)
		sbolDoc.name = "ThroughputTest_Coll_" + str(i) + "_name"
		sbolDoc.description = "ThroughputTest_Coll_" + str(i) + "_description"
		doc_list.append(sbolDoc)
	return doc_list

def run_tests(iterations=0, testType=0):
	sbolFile = 'examples/rule30-Q0-v2.xml' 
	SynBioHubUtil.login_sbh()

	sbh_connector = PartShop("https://synbiohub.bbn.com/")
	sbh_user = input('Enter SynBioHub Username: ')
	sbh_connector.login(sbh_user, getpass.getpass(prompt='Enter SynBioHub Password: ', stream=sys.stderr))
	
	if number < 0 or number > 2:
		raise ValueError("Error: testType must be 0, 1, or 2")

	isSpeed = (testType == 0) or (testType == 2)
	isThrpt = (testType == 1) or (testType == 2)
	
	if isSpeed:
		pullTimes, pushTimes = testSpeed(iterations, sbolDoc, sbh_connector)
		df = pd.DataFrame({"Pull Time": pullTimes,
							"Push Time": pushTimes})
		fig, ax = plt.subplots()
		ax.set_title("Speed Test")
		ax.set_ylabel("Time (sec)")
		ax.set_xlabel("Iterations")
		df.plot(x=df.index, ax = ax)
		plt.show()
		df.to_csv("test.csv")

	if isThrpt:
		testThroughput(iterations, sbolDoc, sbh_connector)


if __name__ == '__main__':
	run_tests(1, False)
	
