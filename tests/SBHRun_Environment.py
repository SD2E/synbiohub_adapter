
import threading
import time
import pandas as pd

import numpy as np
import matplotlib.cm as cm
import matplotlib.pyplot as plt

import os
import fnmatch
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
            self.pushPull_List.append((push_time, 0))  # TODO: currently pull will not work on current pySBOL build so set to 0
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

    '''
    def __init__(self, xmlFile, uid):
        xmlGraph = Graph()
        xmlGraph.parse(xmlFile)

        total_obj = []
        for sbol_subj, sbol_pred, sbol_obj in xmlGraph:
            total_obj.append(sbol_obj)
        self.__tripleSize = len(total_obj)

        self.__sbolDoc = self.create_sbolDoc(xmlFile, uid)
        self.__sbolFile = xmlFile

    '''
    Returns a new SBOL document created from the given SBOL file and an instance of an SBOLTriple
    '''
    def create_sbolDoc(self, sbolFile, uid):
        sbolDoc = Document()
        sbolDoc.read(sbolFile)

        sbolDoc.displayId = uid
        sbolDoc.name = uid + "_name"
        sbolDoc.description = uid + "_description"
        sbolDoc.version = str("1")

        return sbolDoc

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
        trip_obj = SBOLTriple(sbolFile, uid)
        sbolTriples.append(trip_obj)
        sbolDoc_List.append(trip_obj.sbolDoc())
        print("created doc%s" % i)

    return sbolDoc_List, sbolTriples


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
                    print("Found the wrong SynBioHub Part with this uri: %s" % sbolURI)

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
    currTotal = []
    threads = createThreads(1, sbh_connector, sbolDoc_size, idPrefix + "ST_Coll_", sbolFile)
    for t in threads:
        t.start()

    for t in threads:
        t.join()

    for t in threads:
        sum = 0
        for r1, r2 in t.pushPull_Times():
            pushTimes.append(r1)
            pullTimes.append(r2)
            sum += r1
            currTotal.append(sum)

    df = pd.DataFrame({"Pull_Time": pullTimes,
                       "Push_Time": pushTimes,
                       "Total_Time": currTotal})
    # df.loc['Total'] = df.sum()
    return df

def run_triples(sbh_connector, collPrefix, sbolFiles):
    triples_list = []
    doc = 0
    for s in sbolFiles:
        print(s)
        uid = get_uniqueID(collPrefix + "_t" + str(1) + "_d" + str(doc))
        trip_obj = SBOLTriple(s, uid)
        triples_list.append(trip_obj)
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
        setId_List.extend(["set_t" + str(threadSize)] * len(curr_set))
        threadSize += t_growthRate

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

def generate_tripleData(sbh_connector, iterations, collPrefix, sbolFiles):
    runId_List = []
    tripeSize_List = []
    pushTime_List = []
    for i in range(1, iterations+1):
        sbol_tripleSizes, pushTimes = run_triples(sbh_connector, collPrefix+str(i), sbolFiles)

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
    return file_name

def br_speed(sbh_connector, sbolDoc_size, sbolFiles):
    for f in sbolFiles:
        print(f)
        df = generate_speedData(f, sbh_connector, sbolDoc_size, "RS_")
        fileName = get_fileName(f)
        trip_obj = SBOLTriple(f, "temp_id")
        triple_size = trip_obj.totalTriples()

        create_SpeedLinePlot(df, f, sbolDoc_size, triple_size)
        create_SpeedLine2Plot(df, f, sbolDoc_size, triple_size)
        df.to_csv("outputs/SpeedResult_f%s_d%s.csv" % (fileName, sbolDoc_size))


def br_setThread(sbh_connector, iterations, set_size, t_growthRate, sbolDoc_size, sbolFiles):
    for f in sbolFiles:
        df = generate_setData(sbh_connector, iterations, set_size, t_growthRate, f, sbolDoc_size, "RST_")
        trip_obj = SBOLTriple(f, "temp_id")
        fileName = get_fileName(f)
        create_SetBarPlot(df, iterations, set_size, f, trip_obj.totalTriples(), sbolDoc_size)
        df.to_csv("outputs/Set_f%s_iter%s_s%s_d%s.csv" % (fileName, iterations, set_size, sbolDoc_size))

def br_triples(sbh_connector, iterations, sbolFiles):
    df = generate_tripleData(sbh_connector, iterations, "RT", sbolFiles)
    create_TripleScatterPlot(df, iterations)
    df.to_csv("outputs/Triples_iter%s.csv" % (iterations))

def create_SpeedLinePlot(df, f, sbolDoc_size, trip_size):
    y_max = 20
    fig, ax = plt.subplots()
    plt.ylim((0, y_max))
    ax.set_title("Time to Push %s Triples to SynBioHub" % trip_size)
    ax.set_ylabel("Time to Push (sec)")
    ax.set_xlabel("Push Index")

    df.plot(x=df.index+1, y='Push_Time', ax=ax)

    fileName = get_fileName(f)
    fig.savefig('outputs/SpeedResult_f%s_d%s.pdf' % (fileName, sbolDoc_size))

def create_SpeedLine2Plot(df, f, sbolDoc_size, trip_size):
    fig, ax = plt.subplots()
    ax.set_title("Time to Push %s Triples to SynBioHub" % trip_size)
    ax.set_ylabel("Time to Push (sec)")
    ax.set_xlabel("Push Index")
    df.plot(x=df.index+1, y='Total_Time', ax=ax)

    fileName = get_fileName(f)
    fig.savefig('outputs/SpeedResult2_f%s_d%s.pdf' % (fileName, sbolDoc_size))


def create_SetBarPlot(df, iterations, set_size, f, trip_size, doc_size):
    fig, ax = plt.subplots()
    # max_index = df.groupby(['Run_ID', 'Set_ID'])['Time/Thread'].transform(max) == df['Time/Thread']
    # max_df = df[max_index]
    grouped_max = df.groupby(['Set_ID'])
    means = grouped_max.mean()
    errors = grouped_max.std()

    g = plt.get_cmap('Dark2')
    means.plot.barh(xerr=errors, ax=ax, legend=False, colormap=g)

    ax.set_title("Average Time to Push %s Triples per Thread" % (trip_size))
    ax.set_xlabel("Time to Push (sec)")
    ax.set_ylabel("Thread Group")

    fileName = get_fileName(f)
    fig.savefig('outputs/Set_f%s_iter%s_s%s_d%s.pdf' % (fileName, iterations, set_size, doc_size))

def create_TripleScatterPlot(df, iterations):
    fig, ax = plt.subplots()
    plt.ylim((0, 20))
    grouped_runs = df.groupby('Run_ID')
    for name, group in grouped_runs:
        fit = np.polyfit(group['Triple_Size'], group['Push_Time'], deg=1)
        ax.plot(group['Triple_Size'], fit[0]*group['Triple_Size']+fit[1], color='black')
        ax.scatter(data=group, x='Triple_Size', y='Push_Time', marker='o', c='orange')

    ax.set_title("Time to Push SBOL Documents with Varying Size")
    ax.set_ylabel("Time to Push (sec)")
    ax.set_xlabel("Document Size (# of Triples)")
    fig.savefig('outputs/Triples_iter%s.pdf' % (iterations))

def backup_sequentialLoad():
    # At one point, update pushing to SBH to do something like this so performance doesn't suffer.
    sbolDoc = Document()
    sbolDoc.read("./examples/c_trips10000.xml")
    for i in range(1):
        print(i)
        uid = get_uniqueID("ex_")
        sbolDoc.displayId = uid
        sbolDoc.name = uid + "_name"
        sbolDoc.description = uid + "_description"
        sbolDoc.version = str("1")
        push_sbh(sbolDoc, sbh_connector)


if __name__ == '__main__':
    server_name = "https://synbiohub.bbn.com"
    print("Logging into: " + server_name)
    sbh_connector = PartShop(server_name)
    sbh_user = input('Enter Username: ')
    sbh_connector.login(sbh_user, getpass.getpass(prompt='Enter SynBioHub Password: ', stream=sys.stderr))
    # Config.setOption("verbose", True)

    # sbolFiles = get_sbolList("./examples/workingFiles")
    sbolFiles = ["./examples/c_trips40000.xml"]
    iterations = 1
    sbolDoc_size = 1
    br_speed(sbh_connector, sbolDoc_size, sbolFiles)
    # br_triples(sbh_connector, iterations, sbolFiles)

    # iterations, set_size=10, t_growthRate=5, sbolDoc_size=100
    # br_setThread(sbh_connector, 3, 5, 3, 50, sbolFiles) # TODO: MAKE SURE TO CHANGE COLOR OF BAR GRAPH TO MAKE IT LOOK COOL...
