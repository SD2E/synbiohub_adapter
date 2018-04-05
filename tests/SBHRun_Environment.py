
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
	python -m tests.SBHRun_Environment

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


def generate_speedData(sbolFile, sbh_connector, sbolDoc_size, idPrefix):
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

	df = pd.DataFrame({"Pull_Time": pullTimes,
						"Push_Time": pushTimes})
	df.loc['Total'] = df.sum()
	return df

def run_triples(sbh_connector, collPrefix):
	triples_list = []
	sbolFiles = get_sbolList("./examples")
	doc = 0
	for s in sbolFiles:
		uid = get_uniqueID(collPrefix + "_t" + str(1) + "_d" + str(doc))
		sbolTriple, sbolDoc = create_sbolDoc(s, uid)
		triples_list.append(sbolTriple)
		doc += 1
	t = myThread(triples_list, sbh_connector)
	t.start()
	t.join()

	pushTimes = []
	sbol_tripleSizes = []
	for v1, v2 in t.tripleTime_List():
		pushTimes.append(v1)
		sbol_tripleSizes.append(v2.totalTriples())

	return sbol_tripleSizes, pushTimes


def run_setThreads(sbh_connector, set_size, t_growthRate, sbolFile, sbolDoc_size, collPrefix):
	setId_List = []
	threadId_List = []
	threadDur_List = []
	threadSize = t_growthRate
	for i in range(1, set_size+1):
		curr_set = createThreads(threadSize, sbh_connector, sbolDoc_size, collPrefix, sbolFile)
		for t in curr_set:
			t.start()

		for t in curr_set:
			t.join()

		for t in curr_set:
			t_dur = t.thread_duration()
			threadId_List.append(t.getName())
			threadDur_List.append(t_dur)
		threadSize += t_growthRate
		setId_List.extend(["set_t" + str(threadSize)] * len(curr_set))
				
	return setId_List, threadId_List, threadDur_List

def generate_setData(sbh_connector, iterations, set_size, t_growthRate, sbolFile, sbolDoc_size, collPrefix):
	runId_List = []
	setId_List = []
	threadId_List = []
	threadDur_List = []
	for i in range(1, iterations+1):
		r1, r2, r3 = run_setThreads(sbh_connector, set_size, t_growthRate, sbolFile, sbolDoc_size, collPrefix)
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

def generate_tripleData(sbh_connector, iterations, collPrefix):
	runId_List = []
	tripeSize_List = []
	pushTime_List = []
	for i in range(1, iterations+1):
		sbol_tripleSizes, pushTimes = run_triples(sbh_connector, collPrefix+str(i))
		
		runId_List.extend(['Run' + str(i)] * len(pushTimes))
		tripeSize_List.extend(sbol_tripleSizes)
		pushTime_List.extend(pushTimes)

	df = pd.DataFrame({"Run_ID": runId_List,
						"Triple_Size": tripeSize_List, 
						"Push_Time": pushTime_List},  
						columns=['Run_ID', 'Triple_Size', 'Push_Time'])
	return df

def get_fileName(filePath):
	file_ext = os.path.basename(filePath)
	file_name, f_ext = os.path.splitext(file_ext)
	print(file_name)
	return file_name

def br_speed(sbh_connector, sbolDoc_size):
	sbolFiles = get_sbolList('./examples')
	for f in sbolFiles:

		df = generate_speedData(f, sbh_connector, sbolDoc_size, "RS_")
		
		fig, ax = plt.subplots()
		ax.set_title("Time Taken to Make %s Pushes and Pulls to and from SynBioHub" %sbolDoc_size)
		ax.set_ylabel("Time (sec)")
		ax.set_xlabel("Push Number")
		df.iloc[:-1].plot(x=df.iloc[:-1].index, ax = ax)
	
		fileName = get_fileName(f)
		fig.savefig('outputs/SpeedResult_f%s_d%s.pdf' %(fileName, sbolDoc_size))

		df.to_csv("outputs/SpeedResult_f%s_d%s.csv" %(fileName, sbolDoc_size))

def br_setThread(sbh_connector, iterations, set_size=10, t_growthRate=5, sbolDoc_size=100):
	sbolFiles = get_sbolList('./examples')
	for f in sbolFiles:
		df = generate_setData(sbh_connector, iterations, set_size, t_growthRate, f, sbolDoc_size, "RST_")
		fig, ax = plt.subplots()

		max_index = df.groupby(['Run_ID', 'Set_ID'])['Time/Thread'].transform(max) == df['Time/Thread']
		max_df = df[max_index]
		grouped_max = max_df.groupby(['Set_ID'])
		
		means = grouped_max.mean()
		errors = grouped_max.std()
		means.plot.bar(yerr=errors, ax=ax)

		ax.set_title("Sample Standard Deviation Over %s Runs with Varying Set of Threads" %(iterations))
		ax.set_ylabel("Average Time to Push (sec)")
		ax.set_xlabel("Set of Threads with Longest Run Time")
		fileName = get_fileName(f)
		fig.savefig('outputs/Set_f%s_iter%s_s%s.pdf' %(fileName, iterations, set_size))
		df.to_csv("outputs/Set_f%s_iter%s_s%s.csv" %(fileName, iterations, set_size))

def br_triples(sbh_connector, iterations):
	df = generate_tripleData(sbh_connector, iterations, "RT")
	fig, ax = plt.subplots()
	grouped_runs = df.groupby('Run_ID')
	for name, group in grouped_runs:
		ax.scatter(data=group, x='Triple_Size', y='Push_Time', marker='o', label=name)
		
	ax.set_title("Time to Push SBOL Documents with Varying Size" )
	ax.set_ylabel("Time to Push (sec)")
	ax.set_xlabel("Triple Size")
	plt.legend(loc=2)
		
	fig.savefig('outputs/Triples_iter%s.pdf' %(iterations))
	df.to_csv("outputs/Triples_iter%s.csv" %(iterations))

def run_tests(iterations, sbolDoc_size=0, testType=0, thread_size=1, collPrefix="defId_", sbh_server="https://synbiohub.bbn.com/"):
	sbh_connector = PartShop(sbh_server)
	# sbh_user = input('Enter SynBioHub Username: ')
	sbh_user = 'tramy.t.nguyen@raytheon.com'
	sbh_connector.login(sbh_user, getpass.getpass(prompt='Enter SynBioHub Password: ', stream=sys.stderr))
	# Config.setOption("verbose", True)

	
if __name__ == '__main__':
	print("Logging into BBNs SBH")
	sbh_connector = PartShop("https://synbiohub.bbn.com/")
	sbh_user = input('Enter Username: ')
	sbh_connector.login(sbh_user, getpass.getpass(prompt='Enter SynBioHub Password: ', stream=sys.stderr))

	iterations = 100
	br_speed(sbh_connector, iterations)
	br_triples(sbh_connector, iterations)
	
	#iterations, set_size=10, t_growthRate=5, sbolDoc_size=100
	br_setThread(sbh_connector, iterations, 10, 5, 50)

