
import threading
import time
import getpass
import sys

from sbol import *

exitFlag = 0

class myThread (threading.Thread):
	def __init__(self, sbolDoc, sbh_connector):
		threading.Thread.__init__(self)
		self.sbolDoc = sbolDoc
		self.sbh_connector = sbh_connector

	def run(self):
		print("Started Thread at : %s" %(time.ctime(time.time())))
		push_sbh(self.sbolDoc, self.sbh_connector)
		print("Ended Thread at : %s" %(time.ctime(time.time())))

def create_sbolDocs(numDocs, sbolFile='examples/rule30-Q0-v2.xml'):
	doc_list = []
	for i in range(1,numDocs):
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
	start = time.clock()
	sbh_connector.pull(sbolURI, sbolDoc)
	end = time.clock()
	return end - start 

if __name__ == '__main__':
	doc_list = create_sbolDocs(5)

	sbh_connector = PartShop("https://synbiohub.bbn.com/")
	sbh_user = input('Enter SynBioHub Username: ')
	sbh_connector.login(sbh_user, getpass.getpass(prompt='Enter SynBioHub Password: ', stream=sys.stderr))

	threads = [myThread(sbolDoc, sbh_connector) for sbolDoc in doc_list]
	start = time.clock()
	for t in threads:
		t.start()
	
	for t in threads:
		t.join()
	end = time.clock()
	print("throughputs: %s push per second " %(5/(end-start)))
