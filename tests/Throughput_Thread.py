
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
	sbolTriples: A list of SBOL Triples that stores SBOL documents 
	sbh_connector: An instance of pySBOL's PartShop needed to perform login for pushing and pulling data to and from SynBioHub
	'''
	def __init__(self, sbolTriples, sbh_connector):
		threading.Thread.__init__(self)
		self.sbolTriples_list = sbolTriples
		self.sbh_connector = sbh_connector
		self.thread_start = self.thread_end = 0
		self.tupTime_List = []
		self.pushPull_List = []

	'''
	A default run method that will run after a thread is created and started
	'''
	def run(self):
		self.thread_start = time.clock()
		for sbolTriple in self.sbolTriples_list:
			push_time = push_sbh(sbolTriple.sbolDoc(), self.sbh_connector)
			self.tupTime_List.append((push_time, sbolTriple))
			self.pushPull_List.append((push_time, 0)) # TODO: currently pull will not work on current pySBOL build so set to 0
		self.thread_end = time.clock()

	'''
	Returns the time (seconds) it took to run an instance of this thread
	'''
	def thread_duration(self):
		return self.thread_end - self.thread_start

	'''
	Returns a list of python triples where each Triples are structured as (t1, t2).
	t1 = Time it took for each push
	t2 = An instance of the SBOLTriple class that holds information about the given SBOL file.
	'''
	def tripleTime_List(self):
		return self.tupTime_List

	def pushPull_Times(self):
		return self.pushPull_List


class SBOLTriple():

	'''
	An instance of this class will allow a user to access 3 types of information about an SBOLDocument.
	1. the number of SBOL triples found in a SBOL document, 
	2. the SBOL document object generated from pySBOL, and 
	3. the full path of the XML file used to generate the SBOL document.

	xmlFile: the full path of the SBOL File used to create the SBOL document
	sbolDoc: An instance of the SBOL document
	'''
	def __init__(self, xmlFile, sbolDoc):
		xmlGraph = Graph()
		xmlGraph.parse(xmlFile)
		
		total_obj = []
		for sbol_subj, sbol_pred, sbol_obj in xmlGraph:
			total_obj.append(sbol_obj)
		self.__tripleSize = len(total_obj)
		self.__sbolDoc = sbolDoc
		self.__sbolFile = xmlFile

	# Returns this objects SBOL document
	def sbolDoc(self):
		return self.__sbolDoc

	# Returns a string value of the SBOL file that was assigned to this triple object
	def get_xmlFile(self):
		return self.__sbolFile

	# Returns the total number of SBOL triples found in the given SBOL file
	def totalTriples(self):
		return self.__tripleSize

'''
Generates a unique id
'''
def get_uniqueID(idPrefix):
	t = time.ctime()
	uid = '_'.join([idPrefix, t])
	return re.sub(r'[: ]', '_', uid)

'''
Returns a list of SBOL Documents
numDocs: An integer value to indicate how many SBOL documents this method should create
idPrefix: A unique id prefix to set each SBOL document
sbolFile: the SBOL file to create an SBOL document from
'''
def create_sbolDocs(numDocs, idPrefix, sbolFile):
	sbolDoc_List = []
	sbolTriples = []
	u_counter = 0
	for i in range(0, numDocs):
		uid = get_uniqueID(idPrefix + "_d" + str(i))
		print(uid)
		st, sbolDoc = create_sbolDoc(sbolFile, uid)
		sbolTriples.append(st)
		sbolDoc_List.append(sbolDoc)

	return  sbolDoc_List, sbolTriples

'''
Returns a new SBOL document created from the given SBOL file and an instance of an SBOLTriple
'''
def create_sbolDoc(sbolFile, uid):
	sbolDoc = Document()
	sbolDoc.read(sbolFile)

	sbolDoc.displayId = uid 
	sbolDoc.name = uid + "_name"
	sbolDoc.description = uid + "_description"
	sbolDoc.version = str("1")

	st = SBOLTriple(sbolFile, sbolDoc)
	return st, sbolDoc

'''
Returns the full path of a randomly selected SBOL file found in the given directory
dirLocation: The directory to select a random SBOL file from
'''
def get_randomFile(sbolFiles):
	selectedFile = random.choice(sbolFiles)
	return selectedFile

'''
Returns a list of xml file found in the given directory
'''
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


def createThreads(threadNum, sbh_connector, sbolDoc_size, idPrefix, sbolFile):
	threads = []
	for t in range(threadNum):
		time.sleep(1)
		_, sbolTriples = create_sbolDocs(sbolDoc_size, idPrefix + "_t" + str(t), sbolFile)
		threads.append(myThread(sbolTriples, sbh_connector))
	return threads


def test_Speed(sbolFile, sbh_connector, sbolDoc_size, idPrefix):
	pushTimes = []
	pullTimes = []
	threads = createThreads(1, sbh_connector, sbolDoc_size, idPrefix + "ST_Coll_", sbolFile)
	for t in threads:
		t.start()

	for t in threads:
		t.join()

	for t in threads:
		for r1, r2 in t.pushPull_Times():
			pushTimes.append(r1)
			pullTimes.append(r2)

	df = pd.DataFrame({"Pull Time": pullTimes,
							"Push Time": pushTimes})

	return df

def test_triples(sbh_connector, sbolDoc_size, collPrefix):
	triples_list = []
	for d in range(sbolDoc_size):
		sbolFile = get_randomFile(get_sbolList("./examples"))
		uid = get_uniqueID(collPrefix + "_t" + str(1) + "_d" + str(d))
		sbolTriple, sbolDoc = create_sbolDoc(sbolFile, uid)
		triples_list.append(sbolTriple)
	t = myThread(triples_list, sbh_connector)
	t.start()
	t.join()

	pushTimes = []
	sbol_tripleSizes = []
	for v1, v2 in t.tripleTime_List():
		pushTimes.append(v1)
		sbol_tripleSizes.append(v2.totalTriples())

	return sbol_tripleSizes, pushTimes


def test_threadSets(sbh_connector, thread_size, sbolFile, sbolDoc_size, collPrefix):
	print(sbolFile)
	setId_List = []
	threadId_List = []
	threadDur_List = []
	
	for threadSet_val in range(1, thread_size+1):
		thread_set = createThreads(threadSet_val, sbh_connector, sbolDoc_size, collPrefix, sbolFile)
		for t in thread_set:
			t.start()

		for t in thread_set:
			t.join()

		for t in thread_set:
			t_dur = t.thread_duration()
			threadId_List.append(t.getName())
			threadDur_List.append(t_dur)

		setId_List.extend(["set_t" + str(threadSet_val)] * len(thread_set))
		
	return setId_List, threadId_List, threadDur_List

def run_threadSets(sbh_connector, iterations, thread_size, sbolFile, sbolDoc_size, collPrefix):
	runId_List = []
	setId_List = []
	threadId_List = []
	threadDur_List = []
	for i in range(1, iterations+1):
		r1, r2, r3 = test_threadSets(sbh_connector, thread_size, sbolFile, sbolDoc_size, collPrefix)
		runId_List.extend(['run' + str(i)] * len(r1))
		setId_List.extend(r1)
		threadId_List.extend(r2)
		threadDur_List.extend(r3)

	df = pd.DataFrame({"Run_ID": runId_List,
						"Set_ID": setId_List, 
						"Thread_ID": threadId_List, 
						"Time/Thread": threadDur_List},  
						columns=['Run_ID', 'Set_ID', 'Thread_ID', 'Time/Thread'])
	return df

def run_tripleSize(sbh_connector, iterations, sbolDoc_size, collPrefix):
	
	runId_List = []
	tripeSize_List = []
	pushTime_List = []
	for i in range(1, iterations+1):
		sbol_tripleSizes, pushTimes = test_triples(sbh_connector, sbolDoc_size, collPrefix+str(i))
		
		runId_List.extend(['Run' + str(i)] * len(pushTimes))
		tripeSize_List.extend(sbol_tripleSizes)
		pushTime_List.extend(pushTimes)

	df = pd.DataFrame({"Run_ID": runId_List,
						"Triple_Size": tripeSize_List, 
						"Push_Time": pushTime_List},  
						columns=['Run_ID', 'Triple_Size', 'Push_Time'])

	return df
	
'''
	A method to test the speed and throughput for pushing and pulling data to and from SynBioHub. 
	The test data for each type of testing are written to a csv file.
	PNG figures are also generated for each form of testing. 
	Both the PNG figure and csv are exported in this module's "output" directory

	sbolDoc_size: The number of SBOL documents to create for testing speed and throughput
	testType: An integer value between [0, 3). 0 to run speed, 1 to run throughput, and 2 to run both speed and throughput testing
	thread_size: Number of threads to execute for testing
	collPrefix: A unique id that will be set as the prefix of a SynBioHub collection
	sbh_server: The SynBioHub server that the user would like to push and pull these random testing data to
'''
def run_tests(sbolDoc_size=0, testType=0, thread_size=1, collPrefix="defId_", sbh_server="https://synbiohub.bbn.com/"):
	sbh_connector = PartShop(sbh_server)
	# sbh_user = input('Enter SynBioHub Username: ')
	sbh_user = 'tramy.t.nguyen@raytheon.com'
	sbh_connector.login(sbh_user, getpass.getpass(prompt='Enter SynBioHub Password: ', stream=sys.stderr))
	# Config.setOption("verbose", True)

	if testType < 0 or testType > 2:
		raise ValueError("Error: testType must be 0, 1, or 2")

	isSpeed = (testType == 0) 
	isThreadSet = (testType == 1) 
	isTriple = (testType == 2) 

	sbolFile = get_randomFile(get_sbolList('./examples'))

	if isSpeed:
		df = test_Speed(sbolFile, sbh_connector, sbolDoc_size, collPrefix)
		
		fig, ax = plt.subplots()
		ax.set_title("Time Taken to Make %s Pushes and Pulls to and from SynBioHub" %sbolDoc_size)
		ax.set_ylabel("Time (sec)")
		ax.set_xlabel("# of SBOL Documents")
		df.plot(x=df.index, ax = ax)
		plt.show()
		fig.savefig('outputs/SpeedResult_%s_iter.png' %sbolDoc_size)

		df.loc['Total'] = df.sum()
		df.to_csv("outputs/SpeedResult_%s_iter.csv" %sbolDoc_size)

	elif isThreadSet:
		sbolFile = "examples/r30_t3.xml"
		df = run_threadSets(sbh_connector, 3, thread_size, sbolFile, sbolDoc_size, collPrefix)
		fig, ax = plt.subplots()
		max_index = df.groupby(['Run_ID', 'Set_ID'])['Time/Thread'].transform(max) == df['Time/Thread']
		max_df = df[max_index]
		grouped_max = max_df.groupby('Run_ID')
		for name, group in grouped_max:
			ax.scatter(data=group, x='Set_ID', y='Time/Thread', marker='o', label=name)

		ax.set_title("Longest Time to Push %s SBOL Documents in each Set of Threads" %sbolDoc_size)
		ax.set_ylabel("Longest Push Time Found in each Set (sec)")
		ax.set_xlabel("Set Value")
		plt.legend(loc='best')
		plt.show()
		fig.savefig('outputs/Set_t%s_d%s.png' %(threadNum, sbolDoc_size))
		df.to_csv("outputs/Set_t%s_d%s.csv" %(threadNum, sbolDoc_size))

	elif isTriple:
		iterations = 3
		df = run_tripleSize(sbh_connector, 3, sbolDoc_size, collPrefix)
		fig, ax = plt.subplots()

		grouped_runs = df.groupby('Run_ID')
		for name, group in grouped_runs:
			ax.scatter(data=group, x='Triple_Size', y='Push_Time', marker='o', label=name)
		
		ax.set_title("Time to Push Data for %s SBOL Documents with Varying Size" %sbolDoc_size)
		ax.set_ylabel("Time to Push (sec)")
		ax.set_xlabel("Triple Size")
		plt.legend(loc=2)
		plt.show()
		fig.savefig('outputs/Triples_r%s_d%s.png' %(iterations, sbolDoc_size))
		df.to_csv("outputs/Triples_r%s_d%s.csv" %(iterations, sbolDoc_size))

if __name__ == '__main__':
	docNum = 3 
	testType = 0
	threadNum = 5
	uniqueId = "RT3_m" 
	run_tests(docNum, testType, threadNum, uniqueId)

	# sbh_connector = PartShop('https://synbiohub.bbn.com/')
	# sbh_user = input('Enter SynBioHub Username: ')
	# sbh_connector.login(sbh_user, getpass.getpass(prompt='Enter SynBioHub Password: ', stream=sys.stderr))
	# Config.setOption("verbose", True)

	# uri = 'RT1_cTT_Coll_0_0/transcriptic_rule_30_q0_1_09242017/1'
	# uri2= 'https://synbiohub.bbn.com/user/tramyn/RT1_cTT_Coll_0_0/transcriptic_rule_30_q0_1_09242017/1'
	# pull_sbh(sbh_connector, uri)


