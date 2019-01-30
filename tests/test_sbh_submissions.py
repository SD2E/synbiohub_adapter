# import unittest

# from synbiohub_adapter.query_synbiohub import *
# from synbiohub_adapter.SynBioHubUtil import *
# from sbol import *

# class TestSBHSubmissions(unittest.TestCase):
# 	'''
# 		This class will perform unit testing to submit SBOL data to SynBioHub. 

# 		To run this python file, enter in the following command from the synbiohub_adapter directory:
# 			python -m unittest tests/Test_SBHSubmissions.py
# 	'''

# 	def test_submitNewCollection(self):
# 		server = SBHConstants.BBN_SERVER
# 		sbhQuery = SynBioHubQuery(server)

# 		rule30_sbol = 'examples/rule_30_design.xml'
# 		displayId = 'design'
# 		name = 'BBN_Rule30_Design'
# 		description = 'Rule of 30 design collection used for testing BBN SBH instance'
# 		version = '1'
		
# 		sbolDoc = loadSBOLFile(rule30_sbol)
# 		sbhQuery.submit_NewCollection(sbolDoc, displayId, name, description, version)

# 	def test_submitNewCollection2(self):
# 		server = SBHConstants.BBN_SERVER
# 		sbhQuery = SynBioHubQuery(server)

# 		rule30_sbol = 'examples/rule_30_plan.xml'
# 		displayId = 'transcriptic_rule_30_q0_1_09242017'
# 		name = 'BBN_Rule30_Plan'
# 		description = 'Rule of 30 plan collection used for testing BBN SBH instance'
# 		version = '1'
		
# 		sbolDoc = loadSBOLFile(rule30_sbol)
# 		sbhQuery.submit_NewCollection(sbolDoc, displayId, name, description, version)

# 	def test_submitNewCollection3(self):
# 		server = SBHConstants.BBN_SERVER
# 		sbhQuery = SynBioHubQuery(server)

# 		rule30_sbol = 'examples/rule_30_experiments.xml'
# 		displayId = 'rule_30'
# 		name = 'BBN_Rule30_Problem'
# 		description = 'Rule of 30 problem collection used for testing BBN SBH instance'
# 		version = '1'
		
# 		sbolDoc = loadSBOLFile(rule30_sbol)
# 		sbhQuery.submit_NewCollection(sbolDoc, displayId, name, description, version)

# 	def test_submitNewCollection4(self):
# 		server = SBHConstants.BBN_SERVER
# 		sbhQuery = SynBioHubQuery(server)

# 		rule30_sbol = 'examples/rule30-Q0-v2.xml'
# 		displayId = 'rule_30_Q0_v2'
# 		name = 'BBN_Rule30'
# 		description = 'Rule of 30 problem collection used for stress testing'
# 		version = '1'
		
# 		sbolDoc = loadSBOLFile(rule30_sbol)
# 		sbhQuery.submit_NewCollection(sbolDoc, displayId, name, description, version)

# 	def test_submitExistingCollection(self):
# 		# Note: To run this method, make sure that the collection exist on synbiohub first.
# 		server = SBHConstants.BBN_SERVER
# 		sbhQuery = SynBioHubQuery(server)

# 		rule30_sbol = 'examples/rule30-Q0-v2.xml'
# 		rule30_collection = 'https://synbiohub.bbn.com/user/tramyn/design/design_collection/1'
# 		sbolDoc = loadSBOLFile(rule30_sbol)
# 		sbhQuery.submit_ExistingCollection(sbolDoc, rule30_collection, 2)

# 	def test_stress1(self):
# 		sbolDoc = Document()

# 		for i in range(0, 500):
# 			c_uri = "CompDef" + str(i)
# 			c = ComponentDefinition(c_uri, BIOPAX_DNA, '1.0')
			
# 			s_uri = "Seq" + str(i)
# 			elements = 'atatatatat'
# 			s = Sequence(s_uri, elements, SBOL_ENCODING_IUPAC, "1.0")

# 			c.sequences = s.identity

# 			sbolDoc.addComponentDefinition(c)
# 			sbolDoc.addSequence(s)
			
# 		server = SBHConstants.BBN_SERVER
# 		sbhQuery = SynBioHubQuery(server)
# 		displayId = 'stress1_reg'
# 		name = 'dummy_CompDef'
# 		description = 'A collection full of dummy ComponentDefinitions'
# 		version = '1'
# 		sbhQuery.submit_NewCollection(sbolDoc, displayId, name, description, version)

# 	def test_stress2(self):
# 		# write to new collections with different versions
# 		server = SBHConstants.BBN_SERVER
# 		sbhQuery = SynBioHubQuery(server)
		
# 		rule30_sbol = 'examples/rule30-Q0-v2.xml'
# 		description = "same rule of 30 but different versioning collection."
# 		sbolDoc = loadSBOLFile(rule30_sbol)
# 		sbh_connector = sbhQuery.login_SBH()

# 		sbolDoc.description = description

# 		for v in range(0, 3):
# 			version = str(v)
# 			sbolDoc.version = version
# 			sbolDoc.displayId = 'stress2_reg' + version 
# 			sbolDoc.name = 'rule30_Q0_v' + version

# 			sbhQuery.submit_Collection(sbh_connector, sbolDoc, True, 0)


# if __name__ == '__main__':
# 	unittest.main()