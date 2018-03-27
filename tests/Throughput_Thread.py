
import threading
import time
import pandas as pd

import numpy as np
import matplotlib.cm as cm
import matplotlib.pyplot as plt

import os, fnmatch
import random
import re
import getpass
import sys

from rdflib import Graph
from synbiohub_adapter.SynBioHubUtil import *
from sbol import *

'''
	This class will perform unit testing to query information from SynBioHub's instances. 

	Installation Requirement(s):
	- This test environment requires two third party packages to display plot: 
		1. pip install pandas 
		2. python -mpip install -U matplotlib

	To run this python file, enter in the following command from the synbiohub_adapter directory:
	python -m tests.Throughput_Thread

	author(s) :Tramy Nguyen
'''


class myThread (threading.Thread):
	
	'''
	An instance of this class will allow a user to execute N numbers of pushes to a SynBioHub instance.
	sbolTuples: An instance of the SBOLTuple class that holds information about the given SBOL file.
	sbh_connector: An instance of pySBOL's PartShop needed to perform login for pushing and pulling data to and from SynBioHub
	'''
	def __init__(self, sbolTuples, sbh_connector):
		threading.Thread.__init__(self)
		self.sbolDoc_list = sbolTuples
		self.sbh_connector = sbh_connector
		self.thread_start = self.thread_end = 0
		self.tupTime_List = []

	'''
	A default run method that will run after a thread is created and started
	'''
	def run(self):
		self.thread_start = time.clock()
		for sbolTuple in self.sbolDoc_list:
			push_time = push_sbh(sbolTuple.sbolDoc(), self.sbh_connector)
			
			self.tupTime_List.append((push_time, sbolTuple))

			# uri = sbolDoc.displayId + "/transcriptic_rule_30_q0_1_09242017/1"
			# pull_sbh(self.sbh_connector, uri)
		self.thread_end = time.clock()

	'''
	Returns the time (seconds) it took to run an instance of this thread
	'''
	def thread_duration(self):
		return self.thread_end - self.thread_start

	'''
	Returns a list of python tuples where each Tuples are structed as (t1, t2) where
	t1 = Time it took for each push
	t2 = An instance of the SBOLTuple class that holds information about the given SBOL file.
	'''
	def tupleTime_List(self):
		return self.tupTime_List

'''
An instance of this class will allow a user to access 3 types of information about an SBOLDocument.
1. the number of SBOL tuples found in a SBOL document, 
2. the SBOL document object generated from pySBOL, and 
3. the full path of the XML file used to generate the SBOL document.
'''
class SBOLTuple():

	'''
	xmlFile: the full path of the SBOL File used to create the SBOL document
	sbolDoc: An instance of the SBOL document created from the given xmlFile that was parsed into the SBOL format
	'''
	def __init__(self, xmlFile, sbolDoc):
		xmlGraph = Graph()
		xmlGraph.parse(xmlFile)
		
		total_obj = []
		for sbol_subj, sbol_pred, sbol_obj in xmlGraph:
			total_obj.append(sbol_obj)
		self.__tuplesSize = len(total_obj)
		self.__sbolDoc = sbolDoc
		self.__sbolFile = xmlFile

	# Returns this objects SBOL document
	def sbolDoc(self):
		return self.__sbolDoc

	# Returns a string value of the SBOL file that was assigned to this tuple object
	def get_xmlFile(self):
		return self.__sbolFile

	# Returns the total number of SBOL tuples found in the given SBOL file
	def totalTuples(self):
		return self.__tuplesSize

'''
Returns a list of SBOL Documents that were created from SBOL files taken from the "examples" directory of the synbiohub_adapter project

numDocs: An integer value to indicate how many SBOL documents this method should create
collPrefix: A unique prefix id to set the name of the SynBioHub collection that will be created for each SBOL document 
'''
def create_sbolDocs(numDocs, collPrefix, threadVal, sbolFile):
	sbolDoc_List = []
	sbolTuples = []
	for i in range(0, numDocs):
		sbolDoc = Document()
		sbolDoc.read(sbolFile)

		uid = get_uniqueID(collPrefix, threadVal, i)
		print(uid)
		sbolDoc.displayId = uid 
		sbolDoc.name = collPrefix + str(i) + "_name"
		sbolDoc.description = collPrefix + str(i) + "_description"
		sbolDoc.version = str(i)

		st = SBOLTuple(sbolFile, sbolDoc)
		sbolTuples.append(st)
		sbolDoc_List.append(sbolDoc)

	return  sbolDoc_List, sbolTuples

'''
Returns the full path of a randomly selected SBOL file found in the given directory

dirLocation: The directory to select a random SBOL file from
'''
def get_randomFile(sbolFiles):
	selectedFile = random.choice(sbolFiles)
	return selectedFile

def get_sbolList(dirLocation):
	for root, dir, files in os.walk(dirLocation):
		sbolFiles = [os.path.abspath(os.path.join(root, fileName)) for fileName in files]
		return sbolFiles


'''
Returns the time (seconds) it takes to make a push to a new Collection on SynBioHub

sbh_connector: An instance of pySBOL's PartShop needed to perform login for pushing and pulling data to and from SynBioHub
sbolURI: The URI of the SynBioHub collection or the specific part to be fetched
'''
def push_sbh(sbolDoc, sbh_connector):
	start = time.clock()
	result = sbh_connector.submit(sbolDoc)
	end = time.clock()
	print(result)
	if result != 'Successfully uploaded':
		sys.exit()
	return end - start


'''
Returns the time (seconds) it takes to make a pull from an existing SynBioHub Collection

sbh_connector: An instance of pySBOL's PartShop needed to perform login for pushing and pulling data to and from SynBioHub
sbolURI: The URI of the SynBioHub collection or the specific part to be fetched
'''
def pull_sbh(sbh_connector, sbolURI):
	sbolDoc = Document()
	setHomespace("https://bbn.com")
	start = time.clock()
	sbh_connector.pull(sbolURI, sbolDoc)
	end = time.clock()
	
	if sbolDoc is None:
		print("Found nothing and caused no error.")
	else:
		experimentalData_tl = []
		for tl in sbolDoc:
			if topLevel.type == 'http://sd2e.org#ExperimentalData':
				experimentalData_tl.append(topLevel)
				if len(experimentalData_tl) != 74:
					print("Found the wrong SynBioHub Part with this uri: %s" %sbolURI)

	return end - start

'''
This method will test the speed of pushing and pulling data to and from SynBioHub. 
This method will return two list:
	1. The time it takes to make each push to SynBioHub
	2. The time it takes to make a pull from SynBioHub

sbolDoc_List: A list of SBOL documents to push to SynBioHub
sbh_connector: An instance of pySBOL's PartShop needed to perform login for pushing and pulling data to and from SynBioHub
'''
def testSpeed(sbolDoc_List, sbh_connector):
	pushTimes = []
	pullTimes = []

	for sbolDoc in sbolDoc_List:
		pushTime = push_sbh(sbolDoc, sbh_connector)
		pushTimes.append(pushTime)

		# Grab this specific collection
		uri = sbolDoc.displayId + "/transcriptic_rule_30_q0_1_09242017/1"
		pullTime = pull_sbh(sbh_connector, uri)
		pullTimes.append(pullTime)

	return pullTimes, pushTimes

'''
This method performs throughput testing for pushing data to SynBioHub.
The method will return two types of dictionary. 
	1. the time (seconds) for each thread to execute
	2. the time it takes to push varying tuple size from an SBOL document.

threadNum: The number of threads to create
sbh_connector: An instance of pySBOL's PartShop needed to perform login for pushing and pulling data to and from SynBioHub
docNum: The number of SBOL documents to create for testing
uniqueId: A random prefix to help create a unique id needed to set a SynBioHub collection ID.  
'''
def testThroughput(threadNum, sbh_connector, docNum, uniqueId):
	threads = []
	for t in range(0, threadNum):
		sbolTuples = create_sbolDocs(docNum, uniqueId + "TT_Coll_" + str(t) +"_")
		threads.append(myThread(sbolTuples, sbh_connector))
	
	# Note: Start all threads first then join the threads for termination
	for t in threads:
		t.start()

	thread_duration = {}
	tupleTime_res = {}
	for t in threads:
		thread_duration[t.getName()] = t.thread_duration()
		tupleTime_res[t.getName()] = t.tupleTime_List()
		t.join()
	
	return thread_duration, tupleTime_res

def createThreads(threadNum, sbh_connector, sbolFile, docNum, collPrefix):
	threads = []
	for t in range(threadNum):
		time.sleep(1)
		_, sbolTuples = create_sbolDocs(docNum, collPrefix, t, sbolFile)
		threads.append(myThread(sbolTuples, sbh_connector))
	return threads

'''
	A method to test the speed and throughput for pushing and pulling data to and from SynBioHub. 
	The test data for each type of testing are written to a csv file.
	PNG figures are also generated for each form of testing. 
	Both the PNG figure and csv are exported in this module's "output" directory

	iterations: The number of SBOL documents to create for testing speed and throughput
	testType: An integer value between [0, 3). 0 to run speed, 1 to run throughput, and 2 to run both speed and throughput testing
	threadNum: Number of threads to execute for testing
	uniqueId: A unique id that will be set as the prefix of a SynBioHub collection
	sbh_server: The SynBioHub server that the user would like to push and pull these random testing data to
'''
def run_tests(iterations=0, testType=0, threadNum=1, uniqueId="defId_", sbh_server="https://synbiohub.bbn.com/"):
	sbh_connector = PartShop(sbh_server)
	sbh_user = input('Enter SynBioHub Username: ')
	sbh_connector.login(sbh_user, getpass.getpass(prompt='Enter SynBioHub Password: ', stream=sys.stderr))
	# Config.setOption("verbose", True)

	if testType < 0 or testType > 2:
		raise ValueError("Error: testType must be 0, 1, or 2")

	isSpeed = (testType == 0) or (testType == 2)
	isThrpt = (testType == 1) or (testType == 2)

	sbolFile = get_randomFile(get_sbolList('./examples'))
	# sbolFile = "examples/rule_30_designs.xml"

	if isSpeed:
		sbolDoc_List, sbolTuples = create_sbolDocs(iterations, uniqueId + "ST_Coll_", 0, sbolFile)
		pullTimes, pushTimes = testSpeed(sbolDoc_List, sbh_connector)
		df = pd.DataFrame({"Pull Time": pullTimes,
							"Push Time": pushTimes})
		
		fig, ax = plt.subplots()
		ax.set_title("Time Taken to Make %s Pushes and Pulls to and from SynBioHub" %iterations)
		ax.set_ylabel("Time (sec)")
		ax.set_xlabel("Iterations")
		df.plot(x=df.index, ax = ax)
		plt.show()
		fig.savefig('outputs/SpeedResult_%s_iter.png' %iterations)

		df.loc['Total'] = df.sum()
		df.to_csv("outputs/SpeedResult_%s_iter.csv" %iterations)

	if isThrpt:
		print(sbolFile)
		thread_duration = {}

		for threadSet_val in range(1, threadNum+1):
			thread_set = createThreads(threadSet_val, sbh_connector, sbolFile, iterations, uniqueId)

			for t in thread_set:
				t.start()

			for t in thread_set:
				t.join()

			total_threadTime = 0
			thread_id = "set" + str(threadSet_val)
			for t in thread_set:
				total_threadTime += t.thread_duration()
				
			thread_duration[thread_id] = total_threadTime

		df = pd.DataFrame.from_dict(thread_duration, orient='index')
		# df = pd.DataFrame(thread_duration, index=[0])
		
		fig, ax = plt.subplots()
		ax.set_title("Time Taken to Push %s SBOL Documents for each set of Threads" %iterations)
		ax.set_ylabel("Total Push Time per Set (sec)")
		ax.set_xlabel("# of Sets Executed for %s of Threads Ran per Set" %threadNum)
		df.plot(kind="bar", ax=ax)
		plt.show()
		fig.savefig('outputs/Thread_t%s_d%s.png' %(threadNum, iterations))
		df.to_csv("outputs/Thread_t%s_d%s.csv" %(threadNum, iterations))

def get_uniqueID(prefix, threadValue, docNum):
	t = time.ctime()
	uid = '_'.join([prefix, str(threadValue), t, str(docNum)])
	return re.sub(r'[: ]', '_', uid)

		
def backup_t(self):
	if isThrpt:
		thread_duration, tuple_results = testThroughput(threadNum, sbh_connector, iterations, uniqueId)

		df = pd.DataFrame.from_dict(thread_duration, orient='index')
		df.columns = ['Push Time']
		fig, (ax1, ax2) = plt.subplots(2)
		ax1.set_title("Time Taken to Push %s SBOL Documents per Thread" %iterations)
		ax1.set_ylabel("Duration (sec)")
		ax1.set_xlabel("# of Threads")
		df.plot(ax = ax1)
		df.to_csv("outputs/Thread_t%s_d%s.csv" %(threadNum, iterations))
		
		thread_names = []
		sbol_tupleSizes = []
		sbolFileName = []
		pushTimes = []
		for k, lt in tuple_results.items():
			for v1, v2 in lt:
				thread_names.append(k)
				pushTimes.append(v1)
				sbol_tupleSizes.append(v2.totalTuples())
				sbolFileName.append(v2.get_xmlFile())
			
		df2 = pd.DataFrame({"Thread_Name": thread_names, 
							"File_Name": sbolFileName,
							"Total_Tuples": sbol_tupleSizes, 
							"Push_Time": pushTimes},  
							columns=['Thread_Name', 'File_Name', 'Total_Tuples', 'Push_Time'])
		
		groups = df2.groupby('Thread_Name')
		
		for name, group in groups:
			#Note: color value is set relative to numbers of column stored in dataframe
			group.plot(kind='scatter', x='Total_Tuples', y='Push_Time', ax=ax2, marker='o', label=name, color=np.random.rand(4))
		
			
		ax2.set_title("Time relative to the # of Tuples in an SBOL Document Performing a Push")
		ax2.set_ylabel("Time (sec)")
		ax2.set_xlabel("# of SBOL Tuples")
		ax2.legend()
		plt.show()

		fig.savefig('outputs/ThroughputTime_%s_%s.png' %(threadNum, iterations))
		df2.to_csv("outputs/Tuples_t%s_d%s.csv" %(threadNum, iterations))

if __name__ == '__main__':
	docNum = 2 
	testType = 1 
	threadNum = 5
	uniqueId = "RT3_k" 
	run_tests(docNum, testType, threadNum, uniqueId)


