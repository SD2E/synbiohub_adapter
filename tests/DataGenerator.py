
from sbol import *
import time
from rdflib import Graph
import re


def get_uniqueID(idPrefix):
    t = time.ctime()
    uid = '_'.join([idPrefix, t])
    return re.sub(r'[: ]', '_', uid)


def create_compDef(idPrefix):
    c_uri = get_uniqueID('compDef' + idPrefix)
    compDef = ComponentDefinition(c_uri, BIOPAX_DNA, '1.0')
    return compDef


def create_seq(idPrefix):
    s_uri = get_uniqueID('seq' + idPrefix)
    seq = Sequence(s_uri, 'atatatatatatatatat', SBOL_ENCODING_IUPAC, '1.0')
    return seq


if __name__ == '__main__':
    sbolDoc = Document()
    setHomespace("https://www.bbn.com/")
    for i in range(20000):
        # c = create_compDef(str(i))
        s = create_seq(str(i))
        sbolDoc.addComponentDefinition(c)

    res = sbolDoc.writeString()
    xmlGraph = Graph()
    xmlGraph.parse(data=res)

    total_obj = []
    for sbol_subj, sbol_pred, sbol_obj in xmlGraph:
        total_obj.append(sbol_obj)
    print(len(total_obj))
    sbolDoc.write("examples/c_trips" + str(len(total_obj)) + ".xml")
