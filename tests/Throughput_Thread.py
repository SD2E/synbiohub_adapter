
import threading
import time
import pandas as pd
import matplotlib.pyplot as plt

import getpass
import sys

from rdflib import Graph
from synbiohub_adapter.SynBioHubUtil import *
from sbol import *

# download two third party packages to display plot: 
# 	1. pip install pandas 
#	2. python -mpip install -U matplotlib
# python -m tests.Throughput_Thread

class myThread (threading.Thread):
	def __init__(self, sbolTuples, sbh_connector):
		threading.Thread.__init__(self)
		self.sbolDoc_list = sbolTuples
		self.sbh_connector = sbh_connector
		self.thread_start = self.thread_end = 0
		self.tupTime_List = []

	def run(self):
		self.thread_start = time.clock()
		for sbolTuple in self.sbolDoc_list:
			push_time = push_sbh(sbolTuple.sbolDoc(), self.sbh_connector)
			
			self.tupTime_List.append((sbolTuple.totalTuples(), push_time))

			# uri = sbolDoc.displayId + "/transcriptic_rule_30_q0_1_09242017/1"
			# pull_sbh(self.sbh_connector, uri)
		self.thread_end = time.clock()

	def thread_duration(self):
		return self.thread_end - self.thread_start

	def tupleTime_List(self):
		return self.tupTime_List

class SBOLTuple():
	def __init__(self, xmlFile, sbolDoc):
		xmlGraph = Graph()
		xmlGraph.parse(xmlFile)
		
		total_obj = []
		for sbol_subj, sbol_pred, sbol_obj in xmlGraph:
			total_obj.append(sbol_obj)
		self.__tuplesSize = len(total_obj)
		self.__sbolDoc = sbolDoc

	def sbolDoc(self):
		return self.__sbolDoc

	def totalTuples(self):
		return self.__tuplesSize

def create_sbolDocs(numDocs, collPrefix, sbolFile='examples/rule30-Q0-v2.xml'):
	doc_list = []
	sbolTuples = []
	for i in range(0, numDocs):
		sbolDoc = Document()
		sbolDoc.read(sbolFile)
		sbolDoc.displayId = collPrefix + str(i)
		sbolDoc.name = collPrefix + str(i) + "_name"
		sbolDoc.description = collPrefix + str(i) + "_description"
		sbolDoc.version = str(i)
		doc_list.append(sbolDoc)

		st = SBOLTuple(sbolFile, sbolDoc)
		sbolTuples.append(st)

	return doc_list, sbolTuples

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

def testSpeed(sbolDoc_List, sbh_connector):
	pushTimes = []
	pullTimes = []

	for sbolDoc in sbolDoc_List:
		pushTime = push_sbh(sbolDoc, sbh_connector)
		pushTimes.append(pushTime)

		uri = sbolDoc.displayId + "/transcriptic_rule_30_q0_1_09242017/1"
		pullTime = pull_sbh(sbh_connector, uri)
		pullTimes.append(pullTime)

	return pullTimes, pushTimes

def testThroughput(threadNum, sbh_connector, docNum):
	threads = []
	for t in range(0, threadNum):
		sbolDoc_List, sbolTuples = create_sbolDocs(docNum, "TT2_AColl_" + str(t) +"_")
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



def run_tests(iterations=0, testType=0, threadNum=1):
	sbh_connector = PartShop("https://synbiohub.bbn.com/")
	sbh_user = input('Enter SynBioHub Username: ')
	sbh_connector.login(sbh_user, getpass.getpass(prompt='Enter SynBioHub Password: ', stream=sys.stderr))
	# Config.setOption("verbose", True)

	if testType < 0 or testType > 2:
		raise ValueError("Error: testType must be 0, 1, or 2")

	isSpeed = (testType == 0) or (testType == 2)
	isThrpt = (testType == 1) or (testType == 2)

	if isSpeed:
		sbolDoc_List, sbolTuples = create_sbolDocs(iterations, "ST_PColl_")
		pullTimes, pushTimes = testSpeed(sbolDoc_List, sbh_connector)
		df = pd.DataFrame({"Pull Time": pullTimes,
							"Push Time": pushTimes})
		
		fig, ax = plt.subplots()
		ax.set_title("Speed Test")
		ax.set_ylabel("Time (sec)")
		ax.set_xlabel("Iterations")
		df.plot(x=df.index, ax = ax)
		plt.show()
		fig.savefig('outputs/SpeedResult_%s_iter.png' %iterations)

		df.loc['Total'] = df.sum()
		df.to_csv("outputs/SpeedResult_%s_iter.csv" %iterations)

	if isThrpt:
		thread_duration, tuple_results = testThroughput(threadNum, sbh_connector, iterations)

		df = pd.DataFrame.from_dict(thread_duration, orient='index')
		df.columns = ['Push Time']
		fig, (ax1, ax2) = plt.subplots(2)
		ax1.set_title("Time vs. %s SBOL Documents Pushed for Each Thread" %iterations)
		ax1.set_ylabel("Duration (sec)")
		ax1.set_xlabel("# of Threads")
		df.plot(ax = ax1)
		df.to_csv("outputs/Thread_t%s_d%s.csv" %(threadNum, iterations))
		
		thread_names = []
		sbol_tupleSizes = []
		pushTimes = []
		for k, lt in tuple_results.items():
			thread_names.append(k)
			for v1, v2 in lt:
				sbol_tupleSizes.append(v1)
				pushTimes.append(v2)
			
		df2 = pd.DataFrame({"Thread_Name": thread_names, 
							"Total_Tuples": sbol_tupleSizes, 
							"Push_Time": pushTimes},  
							columns=['Thread_Name', 'Total_Tuples', 'Push_Time'])
		
		groups = df2.groupby('Thread_Name')
		for name, group in groups:
			group.plot(x='Total_Tuples', y='Push_Time', ax=ax2, marker='o', label= name)
	
		ax2.set_title("Push Time vs. # of Tuples in SBOLDocuments")
		ax2.set_ylabel("Time (sec)")
		ax2.set_xlabel("# of SBOL Tuples")
		ax2.legend()
		plt.show()

		fig.savefig('outputs/ThroughputTime_%s_%s.png' %(threadNum, iterations))
		df2.to_csv("outputs/Tuples_t%s_d%s.csv" %(threadNum, iterations))
		
		
if __name__ == '__main__':
	docNum = 1 
	testType = 1
	threadNum = 3
	run_tests(docNum, testType, threadNum)

