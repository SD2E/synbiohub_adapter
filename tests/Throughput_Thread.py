
import threading
import time
import pandas as pd
import matplotlib.pyplot as plt

import getpass
import sys

from synbiohub_adapter.SynBioHubUtil import *
from sbol import *

# download third party package to display plot: pip install pandas
# python -m tests.Throughput_Thread

class myThread (threading.Thread):
	def __init__(self, sbolDoc_list, sbh_connector):
		threading.Thread.__init__(self)
		self.sbolDoc_list = sbolDoc_list
		self.sbh_connector = sbh_connector
		self.thread_start = self.thread_end = 0

	def run(self):
		self.thread_start = time.ctime(time.time())
		for sbolDoc in self.sbolDoc_list:
			push_sbh(sbolDoc, self.sbh_connector)
			uri = sbolDoc.displayId + "/transcriptic_rule_30_q0_1_09242017/1"
			pull_sbh(self.sbh_connector, uri)
		self.thread_end = time.ctime(time.time())

	def thread_times(self):
		return self.thread_start, self.thread_end


def create_sbolDocs(numDocs, collPrefix, sbolFile='examples/rule30-Q0-v2.xml'):
	doc_list = []
	for i in range(0, numDocs):
		sbolDoc = Document()
		sbolDoc.read(sbolFile)
		sbolDoc.displayId = collPrefix + str(i)
		sbolDoc.name = collPrefix + str(i) + "_name"
		sbolDoc.description = collPrefix + str(i) + "_description"
		sbolDoc.version = str(i)
		doc_list.append(sbolDoc)
	return doc_list

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
		sbolDoc_List = create_sbolDocs(docNum, "TT_EColl_" + str(t))
		threads.append(myThread(sbolDoc_List, sbh_connector))
	start = time.clock()
	for t in threads:
		t.start()
	for t in threads:
		t.join()
	end = time.clock()


def run_tests(iterations=0, testType=0):
	sbh_connector = PartShop("https://synbiohub.bbn.com/")
	sbh_user = input('Enter SynBioHub Username: ')
	sbh_connector.login(sbh_user, getpass.getpass(prompt='Enter SynBioHub Password: ', stream=sys.stderr))
	# Config.setOption("verbose", True)

	if testType < 0 or testType > 2:
		raise ValueError("Error: testType must be 0, 1, or 2")

	isSpeed = (testType == 0) or (testType == 2)
	isThrpt = (testType == 1) or (testType == 2)

	if isSpeed:
		sbolDoc_List = create_sbolDocs(iterations, "ST_NColl_")
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
		threadNum = 3
		testThroughput(threadNum, sbh_connector, iterations)

		

		
if __name__ == '__main__':
	run_tests(3, 1)

