
import threading
import time
import pandas as pd
import matplotlib.pyplot as plt

import getpass
import sys

from synbiohub_adapter.SynBioHubUtil import *
from sbol import *

# download third party package: pip install pandas
# python -m tests.Throughput_Thread

class myThread (threading.Thread):
	def __init__(self, sbolDoc, sbh_connector):
		threading.Thread.__init__(self)
		self.sbolDoc = sbolDoc
		self.sbh_connector = sbh_connector
		self.thread_start = self.thread_end = 0

	def run(self):
		# print("Started Thread at : %s" %(time.ctime(time.time())))
		self.thread_start = time.ctime(time.time())
		push_sbh(self.sbolDoc, self.sbh_connector)
		self.thread_end = time.ctime(time.time())
		# print("Ended Thread at : %s" %(time.ctime(time.time())))

	def thread_times(self):
		return self.thread_start, self.thread_end


def create_sbolDocs(numDocs, startIndex, sbolFile='examples/rule30-Q0-v2.xml'):
	doc_list = []
	print("startIndex %s" %startIndex)
	for i in range(startIndex,numDocs):
		sbolDoc = Document()
		sbolDoc.read(sbolFile)
		sbolDoc.displayId = "ThroughputTest_Coll_" + str(i)
		sbolDoc.name = "ThroughputTest_Coll_" + str(i) + "_name"
		sbolDoc.description = "ThroughputTest_Coll_" + str(i) + "_description"
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
	# sbolDoc.writeString()
	return end - start

def testSpeed(iterations, sbolDoc, sbh_connector):
	
	pushTimes = []
	pullTimes = []

	collPrefix = "ST_CColl_"
	# Note:iteration can't be 0 or lower
	for i in range(0,iterations):
		sbolDoc.displayId = collPrefix + str(i)
		sbolDoc.name = collPrefix + str(i) + "_name"
		sbolDoc.version = str(i)
		sbolDoc.description = collPrefix + str(i) + "_description"
		
		pushTime = push_sbh(sbolDoc, sbh_connector)
		pushTimes.append(pushTime)
	
		pullTime = pull_sbh(sbh_connector, sbolDoc.displayId)
		pullTimes.append(0)
		
	return pullTimes, pushTimes

# Calculate how many pull and push were made to SynBioHub for a specified time
# totalTime: How long to push and pull from SynBioHub
def testSpeed2(totalTime, sbolDoc, sbh_connector):
	numPush = 0
	pushTimes = []
	startTime = time.clock()
	coll_id = "TT2_AColl_" + str(numPush)
	while time.clock() - startTime < totalTime:
		sbolDoc.displayId = coll_id
		sbolDoc.name = coll_id + "_name"
		sbolDoc.version = str(numPush)
		sbolDoc.description = coll_id + "_description"
		
		pushTimes.append(push_sbh(sbolDoc, sbh_connector))
		numPush += 1

	print("%d pushes in %d seconds" % (numPush, totalTime))

def run_tests(iterations=0, testType=0):
	sbolFile = 'examples/rule30-Q0-v2.xml' 
	sbolDoc = Document()
	sbolDoc.read(sbolFile)

	sbh_connector = PartShop("https://synbiohub.bbn.com/")
	sbh_user = input('Enter SynBioHub Username: ')
	sbh_connector.login(sbh_user, getpass.getpass(prompt='Enter SynBioHub Password: ', stream=sys.stderr))

	if testType < 0 or testType > 2:
		raise ValueError("Error: testType must be 0, 1, or 2")

	isSpeed = (testType == 0) or (testType == 2)
	isThrpt = (testType == 1) or (testType == 2)

	if isSpeed:
		pullTimes, pushTimes = testSpeed(iterations, sbolDoc, sbh_connector)
		df = pd.DataFrame({"Pull Time": pullTimes,
							"Push Time": pushTimes})
		df.loc['Total'] = df.sum()
		fig, ax = plt.subplots()
		ax.set_title("Speed Test")
		ax.set_ylabel("Time (sec)")
		ax.set_xlabel("Iterations")
		df.plot(x=df.index, ax = ax)
		plt.show()
		fig.savefig('outputs/SpeedResult_%s_iter.png' %iterations)
		df.to_csv("outputs/SpeedResult_%s_iter.csv" %iterations)

	if isThrpt:
		count = 0
		docNum = iterations
		startIndex = 0
		pushSec = []
		tStart = []
		tEnd = []
		while count < 3:
			doc_list = create_sbolDocs(docNum, startIndex)
			threads = [myThread(sbolDoc, sbh_connector) for sbolDoc in doc_list]
			start = time.clock()
			for t in threads:
				t.start()
			for t in threads:
				t.join()
			end = time.clock()
			for t in threads:
				t_start, t_end = t.thread_times()
				tStart.append(t_start)
				tEnd.append(t_end)

			pushSec.append(docNum/(end-start))
			startIndex = docNum
			docNum += 2
			count += 1

		df = pd.DataFrame({"Thread Started": tStart,
							"Thread Ended": tEnd,
							"Push per Sec": pushSec})
		fig, ax = plt.subplots()
		ax.set_title("Throughput_Thread Test")
		ax.set_ylabel("Time (sec)")
		ax.set_xlabel("Iterations")
		df.plot(x=df.index, ax = ax)
		plt.show()
		fig.savefig('SpeedResult_%s_iter.png' %iterations)
		df.to_csv("SpeedResult_%s_iter.csv" %iterations)

		
if __name__ == '__main__':
	# run_tests(3, 0)

	uri = "https://synbiohub.org/public/igem/BBa_K1001755/1"
	Config.setOption("verbose", True)
	sbh_connector = PartShop("https://synbiohub.org/")
	sbh_user = input('Enter SynBioHub Username: ')
	sbh_connector.login(sbh_user, getpass.getpass(prompt='Enter SynBioHub Password: ', stream=sys.stderr))

	pull_sbh(sbh_connector, uri)