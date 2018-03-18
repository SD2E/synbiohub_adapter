
import time
import pandas as pd
import matplotlib.pyplot as plt

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
def testThroughput(iterations, sbolDoc, sbh_connector):
	p = Pool(processes=iterations)
	inputs = []
	doc_list = create_sbolDocs(iterations)
	
	start = time.clock()
	
	# sbol_ = [(s, sbh_connector) for s in doc_list]
	p.map(f, [sbolDoc,sbh_connector])
	# p.map(f, [(x,x) for x in range(5)])
	# p.close()
	# p.join()
	# p.starmap(push_sbh, inputs)
	end = time.clock()
	# print(iterations/(end-start))

def push_sbh_something(args):
	print(args)
	return push_sbh(*args)

def f(arg):
	print("hello")
	# return push_sbh(arg[0], arg[1])

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

def run_tests(iterations=0, speed=True):
	sbolFile = 'examples/rule30-Q0-v2.xml' 
	sbolDoc = Document()
	sbolDoc.read(sbolFile)

	sbh_connector = PartShop("https://synbiohub.bbn.com/")
	sbh_user = input('Enter SynBioHub Username: ')
	sbh_connector.login(sbh_user, getpass.getpass(prompt='Enter SynBioHub Password: ', stream=sys.stderr))

	if speed:
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

	else:
		testThroughput(iterations, sbolDoc, sbh_connector)


if __name__ == '__main__':
	run_tests(1, False)

	thread1 = myThread(1, "Thread-1", 1)
	thread2 = myThread(2, "Thread-2", 2)