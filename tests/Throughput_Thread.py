
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
	sbolTuples: A list of SBOL Tuples that stores SBOL documents 
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
	def  thread_duration(self):
		return self.thread_end - self.thread_start

	'''
	Returns a list of python tuples where each Tuples are structed as (t1, t2) where
	t1 = Time it took for each push
	t2 = An instance of the SBOLTuple class that holds information about the given SBOL file.
	'''
	def tupleTime_List(self):
		return self.tupTime_List


class SBOLTuple():
	'''
	An instance of this class will allow a user to access 3 types of information about an SBOLDocument.
	1. the number of SBOL tuples found in a SBOL document, 
	2. the SBOL document object generated from pySBOL, and 
	3. the full path of the XML file used to generate the SBOL document.
	'''


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

def get_uniqueID(prefix, threadNum, docNum):
	t = time.ctime()
	uid = '_'.join([prefix, str(threadNum), t, str(docNum)])
	return re.sub(r'[: ]', '_', uid)

'''
Returns a list of SBOL Documents that were created from SBOL files taken from the "examples" directory of the synbiohub_adapter project

numDocs: An integer value to indicate how many SBOL documents this method should create
collPrefix: A unique prefix id to set the name of the SynBioHub collection that will be created for each SBOL document 
'''
def create_sbolDocs(numDocs, collPrefix, threadNum, sbolFile):
	sbolDoc_List = []
	sbolTuples = []
	u_counter = 0
	for i in range(0, numDocs):
		uid = get_uniqueID(collPrefix, threadNum, i)
		print(uid)
		st, sbolDoc = create_sbolDoc(sbolFile, uid)
		sbolTuples.append(st)
		sbolDoc_List.append(sbolDoc)

	return  sbolDoc_List, sbolTuples

def create_sbolDoc(sbolFile, uid):
	sbolDoc = Document()
	sbolDoc.read(sbolFile)

	sbolDoc.displayId = uid 
	sbolDoc.name = uid + "_name"
	sbolDoc.description = uid + "_description"
	sbolDoc.version = str("1")

	st = SBOLTuple(sbolFile, sbolDoc)
	return st, sbolDoc

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
Returns a list of threads created with a given number of SBOL documents stored in each thread
'''
def createThreads(threadNum, sbh_connector, sbolDoc_size, collPrefix, sbolFile):
	threads = []
	for t in range(threadNum):
		time.sleep(1)
		_, sbolTuples = create_sbolDocs(sbolDoc_size, collPrefix, t, sbolFile)
		threads.append(myThread(sbolTuples, sbh_connector))
	return threads

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
		sbolDoc_List, sbolTuples = create_sbolDocs(sbolDoc_size, collPrefix + "ST_Coll_", 0, sbolFile)
		pullTimes, pushTimes = testSpeed(sbolDoc_List, sbh_connector)
		df = pd.DataFrame({"Pull Time": pullTimes,
							"Push Time": pushTimes})
		
		fig, ax = plt.subplots()
		ax.set_title("Time Taken to Make %s Pushes and Pulls to and from SynBioHub" %sbolDoc_size)
		ax.set_ylabel("Time (sec)")
		ax.set_xlabel("Iterations")
		df.plot(x=df.index, ax = ax)
		plt.show()
		fig.savefig('outputs/SpeedResult_%s_iter.png' %sbolDoc_size)

		df.loc['Total'] = df.sum()
		df.to_csv("outputs/SpeedResult_%s_iter.csv" %sbolDoc_size)

	if isThrpt:
		# test_threadSets(sbh_connector, thread_size, sbolFile, sbolDoc_size, collPrefix)
		test_triples(sbh_connector, sbolDoc_size, collPrefix)

def test_triples(sbh_connector, sbolDoc_size, collPrefix):
	triples_list = []
	for d in range(sbolDoc_size):
		sbolFile = get_randomFile(get_sbolList("./examples"))
		uid = get_uniqueID(collPrefix, 1, d)
		sbolTuple, sbolDoc = create_sbolDoc(sbolFile, uid)
		triples_list.append(sbolTuple)
	t = myThread(triples_list, sbh_connector)
	t.start()
	t.join()

	pushTimes = []
	sbol_tripleSizes = []
	for v1, v2 in t.tupleTime_List():
		pushTimes.append(v1)
		sbol_tripleSizes.append(v2.totalTuples())

	df = pd.DataFrame({"Triple_Size": sbol_tripleSizes, 
						"Push_Time": pushTimes},  
						columns=['Triple_Size', 'Push_Time'])
	fig, ax = plt.subplots()
	ax.set_title("Time to Push Data to SynBiohub with Varying SBOL Document Size" )
	ax.set_ylabel("Time Taken to Push an SBOL document (sec)")
	ax.set_xlabel("Different Tuple Size of Varying SBOL Documents")
	df.plot(kind='bar', x='Triple_Size', y='Push_Time', ax = ax)
	plt.show()
	fig.savefig('outputs/Triples_d%s.png' %sbolDoc_size)
	df.to_csv("outputs/Triples_d%s.csv" %sbolDoc_size)


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

		curr_setTimes = []
		for t in thread_set:
			t_dur = t.thread_duration()
			threadId_List.append(t.getName())
			threadDur_List.append(t_dur)
			curr_setTimes.append(t_dur)

		setId_List.extend(["set_t" + str(threadSet_val)] * len(thread_set))
		
	df = pd.DataFrame({"Set_ID": setId_List, 
						"Thread_ID": threadId_List, 
						"Time/Thread": threadDur_List},  
						columns=['Set_ID', 'Thread_ID', 'Time/Thread'])
	grouped_maxTime = df.groupby('Set_ID', sort=False)['Time/Thread'].max()
	
	fig, ax = plt.subplots()
	grouped_maxTime.plot(kind="bar", ax=ax, x='Set_ID', y='Time/Thread')
	
	ax.set_title("Longest Time to Push %s SBOL Documents in each Set of Threads" %sbolDoc_size)
	ax.set_ylabel("Longest Push Time Found in each Set (sec)")
	ax.set_xlabel("# of Sets Ran With Incrementing Threads")
	
	plt.show()
	fig.savefig('outputs/Set_t%s_d%s.png' %(threadNum, sbolDoc_size))
	df.to_csv("outputs/Set_t%s_d%s.csv" %(threadNum, sbolDoc_size))
		
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
	uniqueId = "RT3_m" 
	run_tests(docNum, testType, threadNum, uniqueId)


