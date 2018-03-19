import getpass
import sys

from sbol import *

'''
	This is a utility module containing classes with constant variables used for querying SynBioHub information
	
	author(s) : Nicholas Roehner 
				Tramy Nguyen
'''
class SBOLConstants():
	CIRCULAR = ''.join(['<', SO_CIRCULAR, '>'])
	DNA = ''.join(['<', BIOPAX_DNA, '>'])
	SMALL_MOLECULE = ''.join(['<', BIOPAX_SMALL_MOLECULE, '>'])
	EFFECTOR = "<http://identifiers.org/chebi/CHEBI:35224>"
	LOGIC_OPERATOR = "<http://edamontology.org/data_2133>"
	NCIT_STRAIN = "<http://purl.obolibrary.org/obo/NCIT_C14419>"
	OBI_STRAIN = "<http://purl.obolibrary.org/obo/OBI_0001185>"

	SBOL_NS = "http://sbols.org/v2#"
	BBN_HOMESPACE = "https://synbiohub.bbn.com"

class SBHConstants():
	SD2_SERVER = "http://hub-api.sd2e.org:80/sparql"
	BBN_SERVER = "https://synbiohub.bbn.com/"
	BBN_YEASTGATES_COLLECTION = "<https://synbiohub.bbn.com/user/tramyn/BBN_YEAST_GATES/BBN_YEAST_GATES_collection/1>"
	BBN_RULE30_COLLECTION = '<https://synbiohub.bbn.com/user/tramyn/transcriptic_rule_30_q0_1_09242017/transcriptic_rule_30_q0_1_09242017_collection/1>'
	RULE_30_EXPERIMENT_COLLECTION = '<https://hub.sd2e.org/user/sd2e/experiment/rule_30/1>'
	YEAST_GATES_EXPERIMENT_COLLECTION = '<https://hub.sd2e.org/user/sd2e/experiment/yeast_gates/1>'
	RULE_30_DESIGN_COLLECTION = '<https://hub.sd2e.org/user/sd2e/design/rule_30/1>'
	YEAST_GATES_DESIGN_COLLECTION = '<https://hub.sd2e.org/user/sd2e/design/yeast_gates/1>'
	SD2_DESIGN_COLLECTION = '<https://hub.sd2e.org/user/sd2e/design/design_collection/1>'
	SD2_EXPERIMENT_COLLECTION = '<https://hub.sd2e.org/user/sd2e/experiment/experiment_collection/1>'


def loadSBOLFile(sbolFile):
	sbolDoc = Document()
	sbolDoc.read(sbolFile)
	return sbolDoc

def login_SBH(server):
	sbh_connector = PartShop(server)
	sbh_user = input('Enter SynBioHub Username: ')
	sbh_connector.login(sbh_user, getpass.getpass(prompt='Enter SynBioHub Password: ', stream=sys.stderr))
	return sbh_connector