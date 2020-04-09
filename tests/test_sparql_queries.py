import unittest

from synbiohub_adapter.query_synbiohub import *
from synbiohub_adapter.SynBioHubUtil import *
from sbol2 import *
from getpass import getpass
import sys
import os


class TestSBHQueries(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.user = 'sd2e'
        if 'SBH_PASSWORD' in os.environ.keys():
            self.password = os.environ['SBH_PASSWORD']
        else:
            self.password = getpass()

    '''
        This class will perform unit testing to query information from SynBioHub's instances.

        Installation Requirement(s):
        - This test environment will need SPARQLWrapper installed to run successfully.
            SPARQLWrapper is used to remotely execute SynBioHub queries.

        To run this python file, enter in the following command from the synbiohub_adapter directory:
            python -m unittest tests/test_sparql_queries.py

        author(s) : Nicholas Roehner
                    Tramy Nguyen
    '''

    # Test collection query methods \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

    ###########

    # def test_query_collection_members(self):
    #   sbh_query = SynBioHubQuery(SD2Constants.SD2_SERVER)
    #   members = sbh_query.query_collection_members([SD2Constants.YEAST_GATES_DESIGN_COLLECTION],
    #                                                ['https://hub.sd2e.org/user/sd2e/design/UWBF_7376/1',
    #                                                 'https://hub.sd2e.org/user/sd2e/design/pAN4036/1'])
    #   print(members)

    ###########

    # def test_query_collections(self):
    #   sbh_query = SynBioHubQuery(SD2Constants.SD2_SERVER)
    #   members = sbh_query.query_collections([SD2Constants.SD2_DESIGN_COLLECTION,
    #                                          'https://hub.sd2e.org/user/sd2e/design/google/1'])
    #   print(members)

    # Test control query methods \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

    def test_query_design_controls(self):
        sbh_query = SynBioHubQuery(SD2Constants.SD2_SERVER)
        sbh_query.login(self.user, self.password)

        controls = set(sbh_query.query_design_controls(pretty=True))

        min_controls = {
            'https://hub.sd2e.org/user/sd2e/design/fluorescein_control_3_125/1',
            'https://hub.sd2e.org/user/sd2e/design/ludox_S40_control_200/1',
            'https://hub.sd2e.org/user/sd2e/design/water_blank_300/1',
            'https://hub.sd2e.org/user/sd2e/design/fluorescein_control_6_25/1',
            'https://hub.sd2e.org/user/sd2e/design/fluorescein_control_0_05078125/1',
            'https://hub.sd2e.org/user/sd2e/design/fluorescein_control_0_1015625/1',
            'https://hub.sd2e.org/user/sd2e/design/fluorescein_control_0_8125/1',
            'https://hub.sd2e.org/user/sd2e/design/fluorescein_control_1_625/1',
            'https://hub.sd2e.org/user/sd2e/design/fluorescein_control_0_40625/1',
            'https://hub.sd2e.org/user/sd2e/design/fluorescein_control_0_025390625/1',
            'https://hub.sd2e.org/user/sd2e/design/water_blank_200/1',
            'https://hub.sd2e.org/user/sd2e/design/fluorescein_control_0_203125/1',
            'https://hub.sd2e.org/user/sd2e/design/fluorescein_control_50/1',
            'https://hub.sd2e.org/user/sd2e/design/water_blank_100/1',
            'https://hub.sd2e.org/user/sd2e/design/ludox_S40_control_300/1',
            'https://hub.sd2e.org/user/sd2e/design/fluorescein_control_12_5/1',
            'https://hub.sd2e.org/user/sd2e/design/fluorescein_control_25/1',
            'https://hub.sd2e.org/user/sd2e/design/ludox_S40_control_100/1',
            'https://hub.sd2e.org/user/sd2e/design/LB_Cm50_no_inducer/1',
            'https://hub.sd2e.org/user/sd2e/design/spherotech_rainbow_beads/1'
        }

        missing_controls = min_controls.difference(controls)

        msg = "Failed to retrieve {num} of minimum {mini} controls from SD2 program. Missing: {miss}"
        assert len(missing_controls) == 0, msg.format(num=repr(len(min_controls) - len(controls)),
                                                      mini=repr(len(min_controls)),
                                                      miss='\n'.join(missing_controls))

    def test_query_design_set_controls(self):
        sbh_query = SynBioHubQuery(SD2Constants.SD2_SERVER)
        sbh_query.login(self.user, self.password)

        controls = set(sbh_query.query_design_set_controls(SD2Constants.YEAST_GATES_DESIGN_COLLECTION, pretty=True))

        min_controls = {
            'https://hub.sd2e.org/user/sd2e/design/fluorescein_control_3_125/1',
            'https://hub.sd2e.org/user/sd2e/design/ludox_S40_control_200/1',
            'https://hub.sd2e.org/user/sd2e/design/water_blank_300/1',
            'https://hub.sd2e.org/user/sd2e/design/fluorescein_control_6_25/1',
            'https://hub.sd2e.org/user/sd2e/design/fluorescein_control_0_05078125/1',
            'https://hub.sd2e.org/user/sd2e/design/fluorescein_control_0_1015625/1',
            'https://hub.sd2e.org/user/sd2e/design/fluorescein_control_0_8125/1',
            'https://hub.sd2e.org/user/sd2e/design/fluorescein_control_1_625/1',
            'https://hub.sd2e.org/user/sd2e/design/fluorescein_control_0_40625/1',
            'https://hub.sd2e.org/user/sd2e/design/fluorescein_control_0_025390625/1',
            'https://hub.sd2e.org/user/sd2e/design/water_blank_200/1',
            'https://hub.sd2e.org/user/sd2e/design/fluorescein_control_0_203125/1',
            'https://hub.sd2e.org/user/sd2e/design/fluorescein_control_50/1',
            'https://hub.sd2e.org/user/sd2e/design/water_blank_100/1',
            'https://hub.sd2e.org/user/sd2e/design/ludox_S40_control_300/1',
            'https://hub.sd2e.org/user/sd2e/design/fluorescein_control_12_5/1',
            'https://hub.sd2e.org/user/sd2e/design/fluorescein_control_25/1',
            'https://hub.sd2e.org/user/sd2e/design/ludox_S40_control_100/1',
            'https://hub.sd2e.org/user/sd2e/design/spherotech_rainbow_beads/1'
        }

        missing_controls = min_controls.difference(controls)

        msg = "Failed to retrieve {num} of minimum {mini} controls from Yeast Gates challenge problem. Missing: {miss}"
        assert len(missing_controls) == 0, msg.format(num=repr(len(min_controls) - len(controls)),
                                                      mini=repr(len(min_controls)),
                                                      miss='\n'.join(missing_controls))

    def test_query_design_fbead_controls(self):
        sbh_query = SynBioHubQuery(SD2Constants.SD2_SERVER)
        sbh_query.login(self.user, self.password)

        controls = set(sbh_query.query_design_fbead_controls(pretty=True))

        min_controls = {'https://hub.sd2e.org/user/sd2e/design/spherotech_rainbow_beads/1'}

        missing_controls = min_controls.difference(controls)

        msg = "Failed to retrieve {num} of minimum {mini} fluorescent bead controls from SD2 program. Missing: {miss}"
        assert len(missing_controls) == 0, msg.format(num=repr(len(min_controls) - len(controls)),
                                                      mini=repr(len(min_controls)),
                                                      miss='\n'.join(missing_controls))

    def test_query_design_set_fbead_controls(self):
        sbh_query = SynBioHubQuery(SD2Constants.SD2_SERVER)
        sbh_query.login(self.user, self.password)

        controls = set(sbh_query.query_design_set_fbead_controls(SD2Constants.YEAST_GATES_DESIGN_COLLECTION,
                                                                 pretty=True))

        min_controls = {'https://hub.sd2e.org/user/sd2e/design/spherotech_rainbow_beads/1'}

        missing_controls = min_controls.difference(controls)

        msg = "Failed to retrieve {num} of minimum {mini} fluorescent bead"
        msg += " controls from Yeast Gates challenge problem. Missing: {miss}"
        assert len(missing_controls) == 0, msg.format(num=repr(len(min_controls) - len(controls)),
                                                      mini=repr(len(min_controls)),
                                                      miss='\n'.join(missing_controls))

    def test_query_design_fluorescein_controls(self):
        sbh_query = SynBioHubQuery(SD2Constants.SD2_SERVER)
        sbh_query.login(self.user, self.password)

        controls = set(sbh_query.query_design_fluorescein_controls(pretty=True))

        min_controls = {
            'https://hub.sd2e.org/user/sd2e/design/fluorescein_control_3_125/1',
            'https://hub.sd2e.org/user/sd2e/design/fluorescein_control_6_25/1',
            'https://hub.sd2e.org/user/sd2e/design/fluorescein_control_0_05078125/1',
            'https://hub.sd2e.org/user/sd2e/design/fluorescein_control_0_1015625/1',
            'https://hub.sd2e.org/user/sd2e/design/fluorescein_control_0_8125/1',
            'https://hub.sd2e.org/user/sd2e/design/fluorescein_control_1_625/1',
            'https://hub.sd2e.org/user/sd2e/design/fluorescein_control_0_40625/1',
            'https://hub.sd2e.org/user/sd2e/design/fluorescein_control_0_025390625/1',
            'https://hub.sd2e.org/user/sd2e/design/fluorescein_control_0_203125/1',
            'https://hub.sd2e.org/user/sd2e/design/fluorescein_control_50/1',
            'https://hub.sd2e.org/user/sd2e/design/fluorescein_control_12_5/1',
            'https://hub.sd2e.org/user/sd2e/design/fluorescein_control_25/1'
        }

        missing_controls = min_controls.difference(controls)

        msg = "Failed to retrieve {num} of minimum {mini} fluorescein controls from SD2 program. Missing: {miss}"
        assert len(missing_controls) == 0, msg.format(num=repr(len(min_controls) - len(controls)),
                                                      mini=repr(len(min_controls)),
                                                      miss='\n'.join(missing_controls))

    def test_query_design_set_fluorescein_controls(self):
        sbh_query = SynBioHubQuery(SD2Constants.SD2_SERVER)
        sbh_query.login(self.user, self.password)

        controls = set(sbh_query.query_design_set_fluorescein_controls(SD2Constants.YEAST_GATES_DESIGN_COLLECTION,
                                                                       pretty=True))

        min_controls = {
            'https://hub.sd2e.org/user/sd2e/design/fluorescein_control_0_203125/1',
            'https://hub.sd2e.org/user/sd2e/design/fluorescein_control_6_25/1',
            'https://hub.sd2e.org/user/sd2e/design/fluorescein_control_1_625/1',
            'https://hub.sd2e.org/user/sd2e/design/fluorescein_control_0_05078125/1',
            'https://hub.sd2e.org/user/sd2e/design/fluorescein_control_3_125/1',
            'https://hub.sd2e.org/user/sd2e/design/fluorescein_control_0_8125/1',
            'https://hub.sd2e.org/user/sd2e/design/fluorescein_control_0_025390625/1',
            'https://hub.sd2e.org/user/sd2e/design/fluorescein_control_12_5/1',
            'https://hub.sd2e.org/user/sd2e/design/fluorescein_control_0_1015625/1',
            'https://hub.sd2e.org/user/sd2e/design/fluorescein_control_50/1',
            'https://hub.sd2e.org/user/sd2e/design/fluorescein_control_25/1',
            'https://hub.sd2e.org/user/sd2e/design/fluorescein_control_0_40625/1'
        }

        missing_controls = min_controls.difference(controls)

        msg = "Failed to retrieve {num} of minimum {mini} fluorescein controls from"
        msg += " Yeast Gates challenge problem. Missing: {miss}"
        assert len(missing_controls) == 0, msg.format(num=repr(len(min_controls) - len(controls)),
                                                      mini=repr(len(min_controls)),
                                                      miss='\n'.join(missing_controls))

    def test_query_design_ludox_controls(self):
        sbh_query = SynBioHubQuery(SD2Constants.SD2_SERVER)
        sbh_query.login(self.user, self.password)

        controls = set(sbh_query.query_design_ludox_controls(pretty=True))

        min_controls = {
            'https://hub.sd2e.org/user/sd2e/design/ludox_S40_control_200/1',
            'https://hub.sd2e.org/user/sd2e/design/ludox_S40_control_300/1',
            'https://hub.sd2e.org/user/sd2e/design/ludox_S40_control_100/1'
        }

        missing_controls = min_controls.difference(controls)

        msg = "Failed to retrieve {num} of minimum {mini} LUDOX controls from SD2 program. Missing: {miss}"
        assert len(missing_controls) == 0, msg.format(num=repr(len(min_controls) - len(controls)),
                                                      mini=repr(len(min_controls)),
                                                      miss='\n'.join(missing_controls))

    def test_query_design_set_ludox_controls(self):
        sbh_query = SynBioHubQuery(SD2Constants.SD2_SERVER)
        sbh_query.login(self.user, self.password)

        controls = set(sbh_query.query_design_set_ludox_controls(SD2Constants.YEAST_GATES_DESIGN_COLLECTION,
                                                                 pretty=True))

        min_controls = {
            'https://hub.sd2e.org/user/sd2e/design/ludox_S40_control_100/1',
            'https://hub.sd2e.org/user/sd2e/design/ludox_S40_control_200/1',
            'https://hub.sd2e.org/user/sd2e/design/ludox_S40_control_300/1'
        }

        missing_controls = min_controls.difference(controls)

        msg = "Failed to retrieve {num} of minimum {mini} LUDOX controls from Yeast Gates challenge problem. Missing: {miss}"
        assert len(missing_controls) == 0, msg.format(num=repr(len(min_controls) - len(controls)),
                                                      mini=repr(len(min_controls)),
                                                      miss='\n'.join(missing_controls))

    def test_query_design_water_controls(self):
        sbh_query = SynBioHubQuery(SD2Constants.SD2_SERVER)
        sbh_query.login(self.user, self.password)

        controls = set(sbh_query.query_design_water_controls(pretty=True))

        min_controls = {
            'https://hub.sd2e.org/user/sd2e/design/water_blank_300/1',
            'https://hub.sd2e.org/user/sd2e/design/water_blank_200/1',
            'https://hub.sd2e.org/user/sd2e/design/water_blank_100/1'
        }

        missing_controls = min_controls.difference(controls)

        msg = "Failed to retrieve {num} of minimum {mini} water controls from SD2 program. Missing: {miss}"
        assert len(missing_controls) == 0, msg.format(num=repr(len(min_controls) - len(controls)),
                                                      mini=repr(len(min_controls)),
                                                      miss='\n'.join(missing_controls))

    def test_query_design_set_water_controls(self):
        sbh_query = SynBioHubQuery(SD2Constants.SD2_SERVER)
        sbh_query.login(self.user, self.password)

        controls = set(sbh_query.query_design_set_water_controls(SD2Constants.YEAST_GATES_DESIGN_COLLECTION,
                                                                 pretty=True))

        min_controls = {
            'https://hub.sd2e.org/user/sd2e/design/water_blank_300/1',
            'https://hub.sd2e.org/user/sd2e/design/water_blank_100/1',
            'https://hub.sd2e.org/user/sd2e/design/water_blank_200/1'
        }

        missing_controls = min_controls.difference(controls)

        msg = "Failed to retrieve {num} of minimum {mini} water controls from Yeast Gates challenge problem. Missing: {miss}"
        assert len(missing_controls) == 0, msg.format(num=repr(len(min_controls) - len(controls)),
                                                      mini=repr(len(min_controls)),
                                                      miss='\n'.join(missing_controls))

    def test_query_experiment_controls(self):
        sbh_query = SynBioHubQuery(SD2Constants.SD2_SERVER)
        sbh_query.login(self.user, self.password)

        controls = set(sbh_query.query_experiment_controls())

        min_controls = {
            'https://hub.sd2e.org/user/sd2e/design/fluorescein_control_3_125/1',
            'https://hub.sd2e.org/user/sd2e/design/ludox_S40_control_200/1',
            'https://hub.sd2e.org/user/sd2e/design/water_blank_300/1',
            'https://hub.sd2e.org/user/sd2e/design/fluorescein_control_6_25/1',
            'https://hub.sd2e.org/user/sd2e/design/fluorescein_control_0_05078125/1',
            'https://hub.sd2e.org/user/sd2e/design/fluorescein_control_0_1015625/1',
            'https://hub.sd2e.org/user/sd2e/design/fluorescein_control_0_8125/1',
            'https://hub.sd2e.org/user/sd2e/design/fluorescein_control_1_625/1',
            'https://hub.sd2e.org/user/sd2e/design/fluorescein_control_0_40625/1',
            'https://hub.sd2e.org/user/sd2e/design/fluorescein_control_0_025390625/1',
            'https://hub.sd2e.org/user/sd2e/design/water_blank_200/1',
            'https://hub.sd2e.org/user/sd2e/design/fluorescein_control_0_203125/1',
            'https://hub.sd2e.org/user/sd2e/design/fluorescein_control_50/1',
            'https://hub.sd2e.org/user/sd2e/design/water_blank_100/1',
            'https://hub.sd2e.org/user/sd2e/design/ludox_S40_control_300/1',
            'https://hub.sd2e.org/user/sd2e/design/fluorescein_control_12_5/1',
            'https://hub.sd2e.org/user/sd2e/design/fluorescein_control_25/1',
            'https://hub.sd2e.org/user/sd2e/design/ludox_S40_control_100/1'
        }

        missing_controls = min_controls.difference(controls)

        assert len(missing_controls) == 0, "Failed to retrieve {num} of minimum {mini} controls from SD2 experiments. Missing: {miss}".format(num=repr(len(min_controls) - len(controls)), mini=repr(len(min_controls)), miss='\n'.join(missing_controls))

    def test_query_experiment_set_controls(self):
        sbh_query = SynBioHubQuery(SD2Constants.SD2_SERVER)
        sbh_query.login(self.user, self.password)

        controls = set(sbh_query.query_experiment_set_controls(SD2Constants.YEAST_GATES_EXPERIMENT_COLLECTION))

        min_controls = {
            'https://hub.sd2e.org/user/sd2e/design/water_blank_300/1',
            'https://hub.sd2e.org/user/sd2e/design/fluorescein_control_3_125/1',
            'https://hub.sd2e.org/user/sd2e/design/ludox_S40_control_200/1',
            'https://hub.sd2e.org/user/sd2e/design/fluorescein_control_6_25/1',
            'https://hub.sd2e.org/user/sd2e/design/fluorescein_control_0_05078125/1',
            'https://hub.sd2e.org/user/sd2e/design/fluorescein_control_0_40625/1',
            'https://hub.sd2e.org/user/sd2e/design/fluorescein_control_0_1015625/1',
            'https://hub.sd2e.org/user/sd2e/design/fluorescein_control_0_8125/1',
            'https://hub.sd2e.org/user/sd2e/design/fluorescein_control_1_625/1',
            'https://hub.sd2e.org/user/sd2e/design/fluorescein_control_0_025390625/1',
            'https://hub.sd2e.org/user/sd2e/design/fluorescein_control_50/1',
            'https://hub.sd2e.org/user/sd2e/design/fluorescein_control_0_203125/1',
            'https://hub.sd2e.org/user/sd2e/design/water_blank_200/1',
            'https://hub.sd2e.org/user/sd2e/design/water_blank_100/1',
            'https://hub.sd2e.org/user/sd2e/design/ludox_S40_control_100/1',
            'https://hub.sd2e.org/user/sd2e/design/fluorescein_control_12_5/1',
            'https://hub.sd2e.org/user/sd2e/design/ludox_S40_control_300/1',
            'https://hub.sd2e.org/user/sd2e/design/fluorescein_control_25/1'
        }

        missing_controls = min_controls.difference(controls)

        assert len(missing_controls) == 0, "Failed to retrieve {num} of minimum {mini} controls from Yeast Gates experiments. Missing: {miss}".format(num=repr(len(min_controls) - len(controls)), mini=repr(len(min_controls)), miss='\n'.join(missing_controls))

    def test_query_single_experiment_controls(self):
        yeast_gates_experiment = 'https://hub.sd2e.org/user/sd2e/experiment/transcriptic_yeast_gates_q0_r1bfbfd7f8dn5/1'

        sbh_query = SynBioHubQuery(SD2Constants.SD2_SERVER)
        sbh_query.login(self.user, self.password)

        controls = sbh_query.query_single_experiment_controls(yeast_gates_experiment)

        min_controls = 72

        assert len(controls) >= min_controls, "Failed to retrieve {num} of {mini} control samples from Yeast Gates experiment {exp}.".format(num=repr(72 - len(controls)), mini=repr(min_controls), exp=yeast_gates_experiment.split('/')[-2])

    # def test_query_experiment_fbead_controls(self):
    #   sbh_query = SynBioHubQuery(SD2Constants.SD2_SERVER)
    #   controls = sbh_query.query_experiment_fbead_controls()

    # def test_query_experiment_set_fbead_controls(self):
    #   sbh_query = SynBioHubQuery(SD2Constants.SD2_SERVER)
    #   controls = sbh_query.query_experiment_set_fbead_controls(SD2Constants.YEAST_GATES_EXPERIMENT_COLLECTION)

    # def test_query_single_experiment_fbead_controls(self):
    #   yeast_gates_experiment = 'https://hub.sd2e.org/user/sd2e/experiment/transcriptic_yeast_gates_q0_r1bfbfd7f8dn5/1'

    #   sbh_query = SynBioHubQuery(SD2Constants.SD2_SERVER)
    #   controls = sbh_query.query_single_experiment_fbead_controls(yeast_gates_experiment)

    def test_query_experiment_fluorescein_controls(self):
        sbh_query = SynBioHubQuery(SD2Constants.SD2_SERVER)
        sbh_query.login(self.user, self.password)

        controls = set(sbh_query.query_experiment_fluorescein_controls())

        min_controls = {
            'https://hub.sd2e.org/user/sd2e/design/fluorescein_control_3_125/1',
            'https://hub.sd2e.org/user/sd2e/design/fluorescein_control_6_25/1',
            'https://hub.sd2e.org/user/sd2e/design/fluorescein_control_0_1015625/1',
            'https://hub.sd2e.org/user/sd2e/design/fluorescein_control_0_05078125/1',
            'https://hub.sd2e.org/user/sd2e/design/fluorescein_control_0_8125/1',
            'https://hub.sd2e.org/user/sd2e/design/fluorescein_control_1_625/1',
            'https://hub.sd2e.org/user/sd2e/design/fluorescein_control_0_40625/1',
            'https://hub.sd2e.org/user/sd2e/design/fluorescein_control_0_025390625/1',
            'https://hub.sd2e.org/user/sd2e/design/fluorescein_control_0_203125/1',
            'https://hub.sd2e.org/user/sd2e/design/fluorescein_control_12_5/1',
            'https://hub.sd2e.org/user/sd2e/design/fluorescein_control_50/1',
            'https://hub.sd2e.org/user/sd2e/design/fluorescein_control_25/1'
        }

        missing_controls = min_controls.difference(controls)

        assert len(missing_controls) == 0, "Failed to retrieve {num} of minimum {mini} fluorescein controls from SD2 experiments. Missing: {miss}".format(num=repr(len(min_controls) - len(controls)), mini=repr(len(min_controls)), miss='\n'.join(missing_controls))

    def test_query_experiment_set_fluorescein_controls(self):
        sbh_query = SynBioHubQuery(SD2Constants.SD2_SERVER)
        sbh_query.login(self.user, self.password)

        controls = set(sbh_query.query_experiment_set_fluorescein_controls(SD2Constants.YEAST_GATES_EXPERIMENT_COLLECTION))

        min_controls = {
            'https://hub.sd2e.org/user/sd2e/design/fluorescein_control_3_125/1',
            'https://hub.sd2e.org/user/sd2e/design/fluorescein_control_6_25/1',
            'https://hub.sd2e.org/user/sd2e/design/fluorescein_control_0_1015625/1',
            'https://hub.sd2e.org/user/sd2e/design/fluorescein_control_0_05078125/1',
            'https://hub.sd2e.org/user/sd2e/design/fluorescein_control_0_8125/1',
            'https://hub.sd2e.org/user/sd2e/design/fluorescein_control_1_625/1',
            'https://hub.sd2e.org/user/sd2e/design/fluorescein_control_0_40625/1',
            'https://hub.sd2e.org/user/sd2e/design/fluorescein_control_0_203125/1',
            'https://hub.sd2e.org/user/sd2e/design/fluorescein_control_0_025390625/1',
            'https://hub.sd2e.org/user/sd2e/design/fluorescein_control_50/1',
            'https://hub.sd2e.org/user/sd2e/design/fluorescein_control_12_5/1',
            'https://hub.sd2e.org/user/sd2e/design/fluorescein_control_25/1'
        }

        missing_controls = min_controls.difference(controls)

        assert len(missing_controls) == 0, "Failed to retrieve {num} of minimum {mini} fluorescein controls from Yeast Gates experiments. Missing: {miss}".format(num=repr(len(min_controls) - len(controls)), mini=repr(len(min_controls)), miss='\n'.join(missing_controls))

    def test_query_single_experiment_fluorescein_controls(self):
        yeast_gates_experiment = 'https://hub.sd2e.org/user/sd2e/experiment/transcriptic_yeast_gates_q0_r1bfbfd7f8dn5/1'

        sbh_query = SynBioHubQuery(SD2Constants.SD2_SERVER)
        sbh_query.login(self.user, self.password)

        controls = sbh_query.query_single_experiment_fluorescein_controls(yeast_gates_experiment)

        min_controls = 48

        assert len(controls) >= min_controls, "Failed to retrieve {num} of {mini} fluorescein control samples from Yeast Gates experiment {exp}.".format(num=repr(48 - len(controls)), mini=repr(min_controls), exp=yeast_gates_experiment.split('/')[-2])

    def test_query_experiment_ludox_controls(self):
        sbh_query = SynBioHubQuery(SD2Constants.SD2_SERVER)
        sbh_query.login(self.user, self.password)

        controls = set(sbh_query.query_experiment_ludox_controls())

        min_controls = {
            'https://hub.sd2e.org/user/sd2e/design/ludox_S40_control_200/1',
            'https://hub.sd2e.org/user/sd2e/design/ludox_S40_control_300/1',
            'https://hub.sd2e.org/user/sd2e/design/ludox_S40_control_100/1'
        }

        missing_controls = min_controls.difference(controls)

        assert len(missing_controls) == 0, "Failed to retrieve {num} of minimum {mini} LUDOX controls from SD2 experiments. Missing: {miss}".format(num=repr(len(min_controls) - len(controls)), mini=repr(len(min_controls)), miss='\n'.join(missing_controls))

    def test_query_experiment_set_ludox_controls(self):
        sbh_query = SynBioHubQuery(SD2Constants.SD2_SERVER)
        sbh_query.login(self.user, self.password)

        controls = set(sbh_query.query_experiment_set_ludox_controls(SD2Constants.YEAST_GATES_EXPERIMENT_COLLECTION))

        min_controls = {
            'https://hub.sd2e.org/user/sd2e/design/ludox_S40_control_200/1',
            'https://hub.sd2e.org/user/sd2e/design/ludox_S40_control_300/1',
            'https://hub.sd2e.org/user/sd2e/design/ludox_S40_control_100/1'
        }

        missing_controls = min_controls.difference(controls)

        assert len(missing_controls) == 0, "Failed to retrieve {num} of minimum {mini} LUDOX controls from Yeast Gates experiments. Missing: {miss}".format(num=repr(len(min_controls) - len(controls)), mini=repr(len(min_controls)), miss='\n'.join(missing_controls))

    def test_query_single_experiment_ludox_controls(self):
        yeast_gates_experiment = 'https://hub.sd2e.org/user/sd2e/experiment/transcriptic_yeast_gates_q0_r1bfbfd7f8dn5/1'

        sbh_query = SynBioHubQuery(SD2Constants.SD2_SERVER)
        sbh_query.login(self.user, self.password)

        controls = sbh_query.query_single_experiment_ludox_controls(yeast_gates_experiment)

        min_controls = 12

        assert len(controls) >= min_controls, "Failed to retrieve {num} of {mini} LUDOX control samples from Yeast Gates experiment {exp}.".format(num=repr(12 - len(controls)), mini=repr(min_controls), exp=yeast_gates_experiment.split('/')[-2])

    def test_query_experiment_water_controls(self):
        sbh_query = SynBioHubQuery(SD2Constants.SD2_SERVER)
        sbh_query.login(self.user, self.password)

        controls = set(sbh_query.query_experiment_water_controls())

        min_controls = {
            'https://hub.sd2e.org/user/sd2e/design/water_blank_300/1',
            'https://hub.sd2e.org/user/sd2e/design/water_blank_200/1',
            'https://hub.sd2e.org/user/sd2e/design/water_blank_100/1'
        }

        missing_controls = min_controls.difference(controls)

        assert len(missing_controls) == 0, "Failed to retrieve {num} of minimum {mini} water controls from SD2 experiments. Missing: {miss}".format(num=repr(len(min_controls) - len(controls)), mini=repr(len(min_controls)), miss='\n'.join(missing_controls))

    def test_query_experiment_set_water_controls(self):
        sbh_query = SynBioHubQuery(SD2Constants.SD2_SERVER)
        sbh_query.login(self.user, self.password)

        controls = set(sbh_query.query_experiment_set_water_controls(SD2Constants.YEAST_GATES_EXPERIMENT_COLLECTION))

        min_controls = {
            'https://hub.sd2e.org/user/sd2e/design/water_blank_300/1',
            'https://hub.sd2e.org/user/sd2e/design/water_blank_200/1',
            'https://hub.sd2e.org/user/sd2e/design/water_blank_100/1'
        }

        missing_controls = min_controls.difference(controls)

        assert len(missing_controls) == 0, "Failed to retrieve {num} of minimum {mini} water controls from Yeast Gates experiments. Missing: {miss}".format(num=repr(len(min_controls) - len(controls)), mini=repr(len(min_controls)), miss='\n'.join(missing_controls))

    def test_query_single_experiment_water_controls(self):
        yeast_gates_experiment = 'https://hub.sd2e.org/user/sd2e/experiment/transcriptic_yeast_gates_q0_r1bfbfd7f8dn5/1'

        sbh_query = SynBioHubQuery(SD2Constants.SD2_SERVER)
        sbh_query.login(self.user, self.password)

        controls = sbh_query.query_single_experiment_water_controls(yeast_gates_experiment)

        min_controls = 12

        assert len(controls) >= min_controls, "Failed to retrieve {num} of {mini} water control samples from Yeast Gates experiment {exp}.".format(num=repr(min_controls - len(controls)), mini=repr(min_controls), exp=yeast_gates_experiment.split('/')[-2])

    # Test gate query methods \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

    ###########

    # def test_query_single_circuit_sample_properties(self):
    #   sbh_query = SynBioHubQuery(SD2Constants.SD2_SERVER)
    #   sample_props = sbh_query.query_gate_input_levels('https://hub.sd2e.org/user/sd2e/transcriptic_yeast_gates_q0_r1bbktv6x4xke/s1871_R5736_R16724_R28544/1')
    #   print(sample_props)

    ###########

    def test_query_gate_logic(self):
        sbh_query = SynBioHubQuery(SD2Constants.SD2_SERVER)
        sbh_query.login(self.user, self.password)
        actual_circuit = sbh_query.query_gate_logic(['https://hub.sd2e.org/user/sd2e/design/UWBF_16969/1'],
                                                    pretty=True)
        expected_circuit = [{'gate': 'https://hub.sd2e.org/user/sd2e/design/UWBF_16969/1',
                             'gate_type': 'http://www.openmath.org/cd/logic1#xor'}]
        assert expected_circuit == actual_circuit

    def test_query_gate_input_levels(self):
        sbh_query = SynBioHubQuery(SD2Constants.SD2_SERVER)
        sbh_query.login(self.user, self.password)
        input_levels = sbh_query.query_gate_input_levels(['https://hub.sd2e.org/user/sd2e/design/UWBF_16969/1'])
        expected_levels_bindings = [{
            'gate': {
                'type': 'uri',
                'value': 'https://hub.sd2e.org/user/sd2e/design/UWBF_16969/1'
            },
            'gate_type': {
                'type': 'uri',
                'value': 'http://www.openmath.org/cd/logic1#xor'
            },
            'input': {
                'type': 'literal',
                'value': 'pADH1:iRGR-r3'
            },
            'level': {
                'type': 'literal',
                'value': '0'
            }
        }, {
            'gate': {
                'type': 'uri',
                'value': 'https://hub.sd2e.org/user/sd2e/design/UWBF_16969/1'
            },
            'gate_type': {
                'type': 'uri',
                'value': 'http://www.openmath.org/cd/logic1#xor'
            },
            'input': {
                'type': 'literal',
                'value': 'pGRR:RGR-r6'
            },
            'level': {
                'type': 'literal',
                'value': '1'
            }
        }]
        assert expected_levels_bindings == input_levels["results"]["bindings"]

    def test_query_design_gates(self):
        sbh_query = SynBioHubQuery(SD2Constants.SD2_SERVER)
        sbh_query.login(self.user, self.password)

        gates = set(sbh_query.query_design_gates(with_role=False, pretty=True))

        min_gates = {
            'https://hub.sd2e.org/user/sd2e/design/UWBF_16967/1',
            'https://hub.sd2e.org/user/sd2e/design/UWBF_5783/1',
            'https://hub.sd2e.org/user/sd2e/design/UWBF_7300/1',
            'https://hub.sd2e.org/user/sd2e/design/UWBF_7374/1',
            'https://hub.sd2e.org/user/sd2e/design/UWBF_8542/1',
            'https://hub.sd2e.org/user/sd2e/design/UWBF_16970/1',
            'https://hub.sd2e.org/user/sd2e/design/UWBF_8544/1',
            'https://hub.sd2e.org/user/sd2e/design/UWBF_5993/1',
            'https://hub.sd2e.org/user/sd2e/design/UWBF_7373/1',
            'https://hub.sd2e.org/user/sd2e/design/UWBF_7376/1',
            'https://hub.sd2e.org/user/sd2e/design/UWBF_16969/1',
            'https://hub.sd2e.org/user/sd2e/design/UWBF_5992/1',
            'https://hub.sd2e.org/user/sd2e/design/UWBF_6389/1',
            'https://hub.sd2e.org/user/sd2e/design/UWBF_6390/1',
            'https://hub.sd2e.org/user/sd2e/design/UWBF_6391/1',
            'https://hub.sd2e.org/user/sd2e/design/UWBF_8231/1',
            'https://hub.sd2e.org/user/sd2e/design/UWBF_8545/1',
            'https://hub.sd2e.org/user/sd2e/design/UWBF_6388/1',
            'https://hub.sd2e.org/user/sd2e/design/UWBF_7299/1',
            'https://hub.sd2e.org/user/sd2e/design/UWBF_7375/1',
            'https://hub.sd2e.org/user/sd2e/design/UWBF_7377/1',
            'https://hub.sd2e.org/user/sd2e/design/UWBF_8225/1',
            'https://hub.sd2e.org/user/sd2e/design/UWBF_8543/1',
            'https://hub.sd2e.org/user/sd2e/design/UWBF_16968/1'
        }

        missing_gates = min_gates.difference(gates)

        assert len(missing_gates) == 0, "Failed to retrieve {num} of minimum {mini} logic gate strains from SD2 program. Missing: {miss}".format(num=repr(len(min_gates) - len(gates)), mini=repr(len(min_gates)), miss='\n'.join(missing_gates))

    def test_query_design_set_gates(self):
        sbh_query = SynBioHubQuery(SD2Constants.SD2_SERVER)
        sbh_query.login(self.user, self.password)

        gates = set(sbh_query.query_design_set_gates(SD2Constants.YEAST_GATES_DESIGN_COLLECTION, with_role=False,
                                                     pretty=True))

        min_gates = {
            'https://hub.sd2e.org/user/sd2e/design/UWBF_16967/1',
            'https://hub.sd2e.org/user/sd2e/design/UWBF_5783/1',
            'https://hub.sd2e.org/user/sd2e/design/UWBF_7300/1',
            'https://hub.sd2e.org/user/sd2e/design/UWBF_7374/1',
            'https://hub.sd2e.org/user/sd2e/design/UWBF_8542/1',
            'https://hub.sd2e.org/user/sd2e/design/UWBF_16970/1',
            'https://hub.sd2e.org/user/sd2e/design/UWBF_8544/1',
            'https://hub.sd2e.org/user/sd2e/design/UWBF_5993/1',
            'https://hub.sd2e.org/user/sd2e/design/UWBF_7373/1',
            'https://hub.sd2e.org/user/sd2e/design/UWBF_7376/1',
            'https://hub.sd2e.org/user/sd2e/design/UWBF_16969/1',
            'https://hub.sd2e.org/user/sd2e/design/UWBF_5992/1',
            'https://hub.sd2e.org/user/sd2e/design/UWBF_6389/1',
            'https://hub.sd2e.org/user/sd2e/design/UWBF_6390/1',
            'https://hub.sd2e.org/user/sd2e/design/UWBF_6391/1',
            'https://hub.sd2e.org/user/sd2e/design/UWBF_8231/1',
            'https://hub.sd2e.org/user/sd2e/design/UWBF_8545/1',
            'https://hub.sd2e.org/user/sd2e/design/UWBF_6388/1',
            'https://hub.sd2e.org/user/sd2e/design/UWBF_7299/1',
            'https://hub.sd2e.org/user/sd2e/design/UWBF_7375/1',
            'https://hub.sd2e.org/user/sd2e/design/UWBF_7377/1',
            'https://hub.sd2e.org/user/sd2e/design/UWBF_8225/1',
            'https://hub.sd2e.org/user/sd2e/design/UWBF_8543/1',
            'https://hub.sd2e.org/user/sd2e/design/UWBF_16968/1'
        }

        missing_gates = min_gates.difference(gates)

        assert len(missing_gates) == 0, "Failed to retrieve {num} of minimum {mini} logic gate strains from Yeast Gates challenge problem. Missing: {miss}".format(num=repr(len(min_gates) - len(gates)), mini=repr(len(min_gates)), miss='\n'.join(missing_gates))

    def test_query_experiment_gates(self):
        sbh_query = SynBioHubQuery(SD2Constants.SD2_SERVER)
        sbh_query.login(self.user, self.password)

        gates = set(sbh_query.query_experiment_gates(with_role=False))

        min_gates = {
            'https://hub.sd2e.org/user/sd2e/design/UWBF_16967/1',
            'https://hub.sd2e.org/user/sd2e/design/UWBF_5783/1',
            'https://hub.sd2e.org/user/sd2e/design/UWBF_7300/1',
            'https://hub.sd2e.org/user/sd2e/design/UWBF_7374/1',
            'https://hub.sd2e.org/user/sd2e/design/UWBF_8542/1',
            'https://hub.sd2e.org/user/sd2e/design/UWBF_16970/1',
            'https://hub.sd2e.org/user/sd2e/design/UWBF_8544/1',
            'https://hub.sd2e.org/user/sd2e/design/UWBF_5993/1',
            'https://hub.sd2e.org/user/sd2e/design/UWBF_7373/1',
            'https://hub.sd2e.org/user/sd2e/design/UWBF_7376/1',
            'https://hub.sd2e.org/user/sd2e/design/UWBF_16969/1',
            'https://hub.sd2e.org/user/sd2e/design/UWBF_5992/1',
            'https://hub.sd2e.org/user/sd2e/design/UWBF_6389/1',
            'https://hub.sd2e.org/user/sd2e/design/UWBF_6390/1',
            'https://hub.sd2e.org/user/sd2e/design/UWBF_6391/1',
            'https://hub.sd2e.org/user/sd2e/design/UWBF_8231/1',
            'https://hub.sd2e.org/user/sd2e/design/UWBF_8545/1',
            'https://hub.sd2e.org/user/sd2e/design/UWBF_6388/1',
            'https://hub.sd2e.org/user/sd2e/design/UWBF_7299/1',
            'https://hub.sd2e.org/user/sd2e/design/UWBF_7375/1',
            'https://hub.sd2e.org/user/sd2e/design/UWBF_7377/1',
            'https://hub.sd2e.org/user/sd2e/design/UWBF_8225/1',
            'https://hub.sd2e.org/user/sd2e/design/UWBF_8543/1',
            'https://hub.sd2e.org/user/sd2e/design/UWBF_16968/1'
        }

        missing_gates = min_gates.difference(gates)

        assert len(missing_gates) == 0, "Failed to retrieve {num} of minimum {mini} logic gate strains from SD2 experiments. Missing: {miss}".format(num=repr(len(min_gates) - len(gates)), mini=repr(len(min_gates)), miss='\n'.join(missing_gates))

    def test_query_experiment_set_gates(self):
        sbh_query = SynBioHubQuery(SD2Constants.SD2_SERVER)
        sbh_query.login(self.user, self.password)

        gates = set(sbh_query.query_experiment_set_gates(SD2Constants.YEAST_GATES_EXPERIMENT_COLLECTION,
                                                         with_role=False))

        min_gates = {
            'https://hub.sd2e.org/user/sd2e/design/UWBF_16967/1',
            'https://hub.sd2e.org/user/sd2e/design/UWBF_5783/1',
            'https://hub.sd2e.org/user/sd2e/design/UWBF_7300/1',
            'https://hub.sd2e.org/user/sd2e/design/UWBF_7374/1',
            'https://hub.sd2e.org/user/sd2e/design/UWBF_8542/1',
            'https://hub.sd2e.org/user/sd2e/design/UWBF_16970/1',
            'https://hub.sd2e.org/user/sd2e/design/UWBF_8544/1',
            'https://hub.sd2e.org/user/sd2e/design/UWBF_5993/1',
            'https://hub.sd2e.org/user/sd2e/design/UWBF_7373/1',
            'https://hub.sd2e.org/user/sd2e/design/UWBF_7376/1',
            'https://hub.sd2e.org/user/sd2e/design/UWBF_16969/1',
            'https://hub.sd2e.org/user/sd2e/design/UWBF_5992/1',
            'https://hub.sd2e.org/user/sd2e/design/UWBF_6389/1',
            'https://hub.sd2e.org/user/sd2e/design/UWBF_6390/1',
            'https://hub.sd2e.org/user/sd2e/design/UWBF_6391/1',
            'https://hub.sd2e.org/user/sd2e/design/UWBF_8231/1',
            'https://hub.sd2e.org/user/sd2e/design/UWBF_8545/1',
            'https://hub.sd2e.org/user/sd2e/design/UWBF_6388/1',
            'https://hub.sd2e.org/user/sd2e/design/UWBF_7299/1',
            'https://hub.sd2e.org/user/sd2e/design/UWBF_7375/1',
            'https://hub.sd2e.org/user/sd2e/design/UWBF_7377/1',
            'https://hub.sd2e.org/user/sd2e/design/UWBF_8225/1',
            'https://hub.sd2e.org/user/sd2e/design/UWBF_8543/1',
            'https://hub.sd2e.org/user/sd2e/design/UWBF_16968/1'
        }

        missing_gates = min_gates.difference(gates)

        assert len(missing_gates) == 0, "Failed to retrieve {num} of minimum {mini} logic gate strains from Yeast Gates experiments. Missing: {miss}".format(num=repr(len(min_gates) - len(gates)), mini=repr(len(min_gates)), miss='\n'.join(missing_gates))

    ###########

    # def test_query_single_experiment_gates(self):
    #   yeast_gates_experiment = 'https://hub.sd2e.org/user/sd2e/experiment/biofab_yeast_gates_q0_aq_11269_4/1'

    #   sbh_query = SynBioHubQuery(SD2Constants.SD2_SERVER)
    #   gates = sbh_query.query_single_experiment_gates(yeast_gates_experiment)

    #   print('0: ' + repr(gates))

    ###########

    # # Test inducer query methods \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

    # def test_query_design_set_inducers(self):
    #   sbh_query = SynBioHubQuery(SD2Constants.SD2_SERVER)
    #   inducers = sbh_query.query_design_set_inducers(SD2Constants.RULE_30_DESIGN_COLLECTION)
    #   print(inducers)

    # def test_query_design_inducers(self):
    #   sbh_query = SynBioHubQuery(SD2Constants.SD2_SERVER)
    #   inducers = sbh_query.query_design_inducers()
    #   print(inducers)

    # def test_query_single_experiment_inducers(self):
    #   rule_30_experiment = 'https://hub.sd2e.org/user/sd2e/experiment/transcriptic_rule_30_q0_1_09242017/1'

    #   sbh_query = SynBioHubQuery(SD2Constants.SD2_SERVER)
    #   inducers = sbh_query.query_single_experiment_inducers(rule_30_experiment)
    #   print(inducers)

    # def test_query_experiment_set_inducers(self):
    #   sbh_query = SynBioHubQuery(SD2Constants.SD2_SERVER)
    #   inducers = sbh_query.query_experiment_set_inducers(SD2Constants.RULE_30_EXPERIMENT_COLLECTION)
    #   print(inducers)

    # def test_query_experiment_inducers(self):
    #   sbh_query = SynBioHubQuery(SD2Constants.SD2_SERVER)
    #   inducers = sbh_query.query_experiment_inducers()
    #   print(inducers)

    # def test_query_sample_inducers(self):
    #   rule_30_sample = 'https://hub.sd2e.org/user/sd2e/transcriptic_rule_30_q0_1_09242017/H07/1'

    #   sbh_query = SynBioHubQuery(SD2Constants.SD2_SERVER)
    #   inducers = sbh_query.query_sample_inducers(rule_30_sample)
    #   print(inducers)

    # def test_query_condition_inducers(self):
    #   rule_30_condition = 'https://hub.sd2e.org/user/sd2e/transcriptic_rule_30_q0_1_09242017/NEB_10_beta_pAN1717_Larabinose_5_aTc_0p002_IPTG_1_system/1'

    #   sbh_query = SynBioHubQuery(SD2Constants.SD2_SERVER)
    #   inducers = sbh_query.query_condition_inducers(rule_30_condition)
    #   print(inducers)

    # # Test media query methods \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

    def test_query_design_media(self):
        sbh_query = SynBioHubQuery(SD2Constants.SD2_SERVER)
        sbh_query.login(self.user, self.password)

        media = set(sbh_query.query_design_media(pretty=True))

        min_media = {
            'https://hub.sd2e.org/user/sd2e/design/CAT_630425/1',
            'https://hub.sd2e.org/user/sd2e/design/CAT_R459942/1',
            'https://hub.sd2e.org/user/sd2e/design/CAT_90000_726/1',
            'https://hub.sd2e.org/user/sd2e/design/CAT_DF0123_17_3/1',
            'https://hub.sd2e.org/user/sd2e/design/culture_media_4/1',
            'https://hub.sd2e.org/user/sd2e/design/M9/1',
            'https://hub.sd2e.org/user/sd2e/design/M90x20Kan0x20500x2Dug0x2Dper0x2DmL/1',
            'https://hub.sd2e.org/user/sd2e/design/M90x20Chlor0x20350x2Dug0x2Dper0x2Dml0x20Kan0x20500x2Dug0x2Dper0x2Dml/1',
            'https://hub.sd2e.org/user/sd2e/design/YEP0x2020x250x2Ddextrose/1',
            'https://hub.sd2e.org/user/sd2e/design/M9_supplemented_no_carbon/1',
            'https://hub.sd2e.org/user/sd2e/design/culture_media_2/1',
            'https://hub.sd2e.org/user/sd2e/design/culture_media_3/1',
            'https://hub.sd2e.org/user/sd2e/design/culture_media_5/1',
            'https://hub.sd2e.org/user/sd2e/design/culture_media_6/1',
            'https://hub.sd2e.org/user/sd2e/design/culture_media_1/1',
            'https://hub.sd2e.org/user/sd2e/design/LB_Cm50_10uM_RDX/1',
            'https://hub.sd2e.org/user/sd2e/design/LB_Cm50_100uM_DNT/1',
            'https://hub.sd2e.org/user/sd2e/design/LB_Broth/1',
            'https://hub.sd2e.org/user/sd2e/design/LB_Cm50_1uM_TNT/1',
            'https://hub.sd2e.org/user/sd2e/design/LB_Cm50_1000uM_TNT/1',
            'https://hub.sd2e.org/user/sd2e/design/LB_Cm50_1uM_RDX/1',
            'https://hub.sd2e.org/user/sd2e/design/LB_Cm50_10uM_TNT/1',
            'https://hub.sd2e.org/user/sd2e/design/LB_Cm50_1000uM_DNT/1',
            'https://hub.sd2e.org/user/sd2e/design/LB_Cm50_100uM_RDX/1',
            'https://hub.sd2e.org/user/sd2e/design/LB_Cm50_10uM_DNT/1',
            'https://hub.sd2e.org/user/sd2e/design/LB_Cm50_100uM_TNT/1',
            'https://hub.sd2e.org/user/sd2e/design/LB_Cm50/1',
            'https://hub.sd2e.org/user/sd2e/design/LB_Cm50_1000uM_RDX/1',
            'https://hub.sd2e.org/user/sd2e/design/LB_Cm50_1uM_DNT/1',
            'https://hub.sd2e.org/user/sd2e/design/culture_media_9/1',
            'https://hub.sd2e.org/user/sd2e/design/culture_media_11/1',
            'https://hub.sd2e.org/user/sd2e/design/culture_media_7/1',
            'https://hub.sd2e.org/user/sd2e/design/culture_media_8/1',
            'https://hub.sd2e.org/user/sd2e/design/culture_media_10/1',
            'https://hub.sd2e.org/user/sd2e/design/culture_media_12/1',
            'https://hub.sd2e.org/user/sd2e/design/teknova_M1902/1',
            'https://hub.sd2e.org/user/sd2e/design/M9_glucose_CAA/1'
        }

        missing_media = min_media.difference(media)

        assert len(missing_media) == 0, "Failed to retrieve {num} of minimum {mini} growth media from SD2 program. Missing: {miss}".format(num=repr(len(min_media) - len(media)), mini=repr(len(min_media)), miss='\n'.join(missing_media))

    def test_query_design_set_media(self):
        sbh_query = SynBioHubQuery(SD2Constants.SD2_SERVER)
        sbh_query.login(self.user, self.password)

        media = set(sbh_query.query_design_set_media(SD2Constants.YEAST_GATES_DESIGN_COLLECTION, pretty=True))

        min_media = {
            'https://hub.sd2e.org/user/sd2e/design/culture_media_4/1',
            'https://hub.sd2e.org/user/sd2e/design/culture_media_2/1',
            'https://hub.sd2e.org/user/sd2e/design/culture_media_3/1',
            'https://hub.sd2e.org/user/sd2e/design/culture_media_5/1',
            'https://hub.sd2e.org/user/sd2e/design/culture_media_6/1',
            'https://hub.sd2e.org/user/sd2e/design/culture_media_1/1',
            'https://hub.sd2e.org/user/sd2e/design/culture_media_9/1',
            'https://hub.sd2e.org/user/sd2e/design/culture_media_11/1',
            'https://hub.sd2e.org/user/sd2e/design/culture_media_7/1',
            'https://hub.sd2e.org/user/sd2e/design/culture_media_8/1',
            'https://hub.sd2e.org/user/sd2e/design/culture_media_10/1',
            'https://hub.sd2e.org/user/sd2e/design/culture_media_12/1'
        }

        missing_media = min_media.difference(media)

        assert len(missing_media) == 0, "Failed to retrieve {num} of minimum {mini} growth media from Yeast Gates challenge problem. Missing: {miss}".format(num=repr(len(min_media) - len(media)), mini=repr(len(min_media)), miss='\n'.join(missing_media))

    def test_query_experiment_media(self):
        sbh_query = SynBioHubQuery(SD2Constants.SD2_SERVER)
        sbh_query.login(self.user, self.password)

        media = set(sbh_query.query_experiment_media())

        min_media = {
            'https://hub.sd2e.org/user/sd2e/design/culture_media_4/1',
            'https://hub.sd2e.org/user/sd2e/design/culture_media_2/1',
            'https://hub.sd2e.org/user/sd2e/design/culture_media_3/1',
            'https://hub.sd2e.org/user/sd2e/design/culture_media_5/1',
            'https://hub.sd2e.org/user/sd2e/design/culture_media_1/1',
            'https://hub.sd2e.org/user/sd2e/design/CAT_DF0123_17_3/1',
            'https://hub.sd2e.org/user/sd2e/design/CAT_90000_726/1',
            'https://hub.sd2e.org/user/sd2e/design/CAT_R459942/1',
            'https://hub.sd2e.org/user/sd2e/design/CAT_630425/1'
        }

        missing_media = min_media.difference(media)

        assert len(missing_media) == 0, "Failed to retrieve {num} of minimum {mini} growth media from SD2 experiments. Missing: {miss}".format(num=repr(len(min_media) - len(media)), mini=repr(len(min_media)), miss='\n'.join(missing_media))

    def test_query_experiment_set_media(self):
        sbh_query = SynBioHubQuery(SD2Constants.SD2_SERVER)
        sbh_query.login(self.user, self.password)

        media = set(sbh_query.query_experiment_set_media(SD2Constants.YEAST_GATES_EXPERIMENT_COLLECTION))

        min_media = {
            'https://hub.sd2e.org/user/sd2e/design/culture_media_4/1',
            'https://hub.sd2e.org/user/sd2e/design/culture_media_2/1',
            'https://hub.sd2e.org/user/sd2e/design/culture_media_3/1',
            'https://hub.sd2e.org/user/sd2e/design/culture_media_5/1',
            'https://hub.sd2e.org/user/sd2e/design/culture_media_1/1',
            'https://hub.sd2e.org/user/sd2e/design/CAT_DF0123_17_3/1',
            'https://hub.sd2e.org/user/sd2e/design/CAT_90000_726/1',
            'https://hub.sd2e.org/user/sd2e/design/CAT_R459942/1',
            'https://hub.sd2e.org/user/sd2e/design/CAT_630425/1'
        }

        missing_media = min_media.difference(media)

        assert len(missing_media) == 0, "Failed to retrieve {num} of minimum {mini} growth media from Yeast Gates experiments. Missing: {miss}".format(num=repr(len(min_media) - len(media)), mini=repr(len(min_media)), miss='\n'.join(missing_media))

    ###########

    # def test_query_single_experiment_media(self):
    #   yeast_gates_experiment = 'https://hub.sd2e.org/user/sd2e/experiment/biofab_yeast_gates_q0_aq_11269_4/1'

    #   sbh_query = SynBioHubQuery(SD2Constants.SD2_SERVER)
    #   media = sbh_query.query_single_experiment_media(yeast_gates_experiment)
    #   print(media)

    # # Test plasmid query methods \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

    def test_query_design_plasmids(self):
        sbh_query = SynBioHubQuery(SD2Constants.SD2_SERVER)
        sbh_query.login(self.user, self.password)

        plasmids = set(sbh_query.query_design_plasmids(pretty=True))

        min_plasmids = {
            'https://hub.sd2e.org/user/sd2e/design/YG_plasmid_002/1',
            'https://hub.sd2e.org/user/sd2e/design/YG_plasmid_013/1',
            'https://hub.sd2e.org/user/sd2e/design/YG_plasmid_014/1',
            'https://hub.sd2e.org/user/sd2e/design/YG_plasmid_017/1',
            'https://hub.sd2e.org/user/sd2e/design/YG_plasmid_023/1',
            'https://hub.sd2e.org/user/sd2e/design/YG_plasmid_021/1',
            'https://hub.sd2e.org/user/sd2e/design/YG_plasmid_004/1',
            'https://hub.sd2e.org/user/sd2e/design/YG_plasmid_011/1',
            'https://hub.sd2e.org/user/sd2e/design/YG_plasmid_024/1',
            'https://hub.sd2e.org/user/sd2e/design/YG_plasmid_019/1',
            'https://hub.sd2e.org/user/sd2e/design/YG_plasmid_003/1',
            'https://hub.sd2e.org/user/sd2e/design/YG_plasmid_016/1',
            'https://hub.sd2e.org/user/sd2e/design/YG_plasmid_010/1',
            'https://hub.sd2e.org/user/sd2e/design/YG_plasmid_012/1',
            'https://hub.sd2e.org/user/sd2e/design/YG_plasmid_018/1',
            'https://hub.sd2e.org/user/sd2e/design/YG_plasmid_009/1',
            'https://hub.sd2e.org/user/sd2e/design/YG_plasmid_022/1',
            'https://hub.sd2e.org/user/sd2e/design/YG_plasmid_008/1',
            'https://hub.sd2e.org/user/sd2e/design/YG_plasmid_007/1',
            'https://hub.sd2e.org/user/sd2e/design/YG_plasmid_015/1',
            'https://hub.sd2e.org/user/sd2e/design/YG_plasmid_001/1',
            'https://hub.sd2e.org/user/sd2e/design/YG_plasmid_006/1',
            'https://hub.sd2e.org/user/sd2e/design/YG_plasmid_020/1',
            'https://hub.sd2e.org/user/sd2e/design/YG_plasmid_005/1',
            'https://hub.sd2e.org/user/sd2e/design/pAN1201/1',
            'https://hub.sd2e.org/user/sd2e/design/pAN1717/1',
            'https://hub.sd2e.org/user/sd2e/design/pAN3928/1',
            'https://hub.sd2e.org/user/sd2e/design/pAN4036/1',
            'https://hub.sd2e.org/user/sd2e/design/YG_plasmid_025/1',
            'https://hub.sd2e.org/user/sd2e/design/pJS007_LALT_NAND/1'
        }

        missing_plasmids = min_plasmids.difference(plasmids)

        assert len(missing_plasmids) == 0, "Failed to retrieve {num} of minimum {mini} plasmids from SD2 program. Missing: {miss}".format(num=repr(len(min_plasmids) - len(plasmids)), mini=repr(len(min_plasmids)), miss='\n'.join(missing_plasmids))

    def test_query_design_set_plasmids(self):
        sbh_query = SynBioHubQuery(SD2Constants.SD2_SERVER)
        sbh_query.login(self.user, self.password)

        plasmids = set(sbh_query.query_design_set_plasmids(SD2Constants.YEAST_GATES_DESIGN_COLLECTION, pretty=True))

        min_plasmids = {
            'https://hub.sd2e.org/user/sd2e/design/YG_plasmid_002/1',
            'https://hub.sd2e.org/user/sd2e/design/YG_plasmid_013/1',
            'https://hub.sd2e.org/user/sd2e/design/YG_plasmid_014/1',
            'https://hub.sd2e.org/user/sd2e/design/YG_plasmid_017/1',
            'https://hub.sd2e.org/user/sd2e/design/YG_plasmid_023/1',
            'https://hub.sd2e.org/user/sd2e/design/YG_plasmid_021/1',
            'https://hub.sd2e.org/user/sd2e/design/YG_plasmid_004/1',
            'https://hub.sd2e.org/user/sd2e/design/YG_plasmid_011/1',
            'https://hub.sd2e.org/user/sd2e/design/YG_plasmid_024/1',
            'https://hub.sd2e.org/user/sd2e/design/YG_plasmid_019/1',
            'https://hub.sd2e.org/user/sd2e/design/YG_plasmid_003/1',
            'https://hub.sd2e.org/user/sd2e/design/YG_plasmid_016/1',
            'https://hub.sd2e.org/user/sd2e/design/YG_plasmid_010/1',
            'https://hub.sd2e.org/user/sd2e/design/YG_plasmid_012/1',
            'https://hub.sd2e.org/user/sd2e/design/YG_plasmid_018/1',
            'https://hub.sd2e.org/user/sd2e/design/YG_plasmid_009/1',
            'https://hub.sd2e.org/user/sd2e/design/YG_plasmid_022/1',
            'https://hub.sd2e.org/user/sd2e/design/YG_plasmid_008/1',
            'https://hub.sd2e.org/user/sd2e/design/YG_plasmid_007/1',
            'https://hub.sd2e.org/user/sd2e/design/YG_plasmid_015/1',
            'https://hub.sd2e.org/user/sd2e/design/YG_plasmid_001/1',
            'https://hub.sd2e.org/user/sd2e/design/YG_plasmid_006/1',
            'https://hub.sd2e.org/user/sd2e/design/YG_plasmid_020/1',
            'https://hub.sd2e.org/user/sd2e/design/YG_plasmid_005/1',
            'https://hub.sd2e.org/user/sd2e/design/YG_plasmid_025/1'
        }

        missing_plasmids = min_plasmids.difference(plasmids)

        assert len(missing_plasmids) == 0, "Failed to retrieve {num} of minimum {mini} plasmids from Yeast Gates challenge problem. Missing: {miss}".format(num=repr(len(min_plasmids) - len(plasmids)), mini=repr(len(min_plasmids)), miss='\n'.join(missing_plasmids))

    def test_query_experiment_plasmids(self):
        sbh_query = SynBioHubQuery(SD2Constants.SD2_SERVER)
        sbh_query.login(self.user, self.password)

        plasmids = set(sbh_query.query_experiment_plasmids())

        min_plasmids = {
            'https://hub.sd2e.org/user/sd2e/design/YG_plasmid_021/1',
            'https://hub.sd2e.org/user/sd2e/design/YG_plasmid_010/1',
            'https://hub.sd2e.org/user/sd2e/design/YG_plasmid_003/1',
            'https://hub.sd2e.org/user/sd2e/design/YG_plasmid_015/1',
            'https://hub.sd2e.org/user/sd2e/design/YG_plasmid_001/1',
            'https://hub.sd2e.org/user/sd2e/design/YG_plasmid_014/1',
            'https://hub.sd2e.org/user/sd2e/design/YG_plasmid_017/1',
            'https://hub.sd2e.org/user/sd2e/design/YG_plasmid_005/1',
            'https://hub.sd2e.org/user/sd2e/design/YG_plasmid_018/1',
            'https://hub.sd2e.org/user/sd2e/design/YG_plasmid_008/1',
            'https://hub.sd2e.org/user/sd2e/design/YG_plasmid_020/1',
            'https://hub.sd2e.org/user/sd2e/design/YG_plasmid_012/1',
            'https://hub.sd2e.org/user/sd2e/design/YG_plasmid_004/1',
            'https://hub.sd2e.org/user/sd2e/design/YG_plasmid_019/1',
            'https://hub.sd2e.org/user/sd2e/design/YG_plasmid_009/1',
            'https://hub.sd2e.org/user/sd2e/design/YG_plasmid_006/1',
            'https://hub.sd2e.org/user/sd2e/design/YG_plasmid_011/1',
            'https://hub.sd2e.org/user/sd2e/design/YG_plasmid_007/1',
            'https://hub.sd2e.org/user/sd2e/design/YG_plasmid_016/1',
            'https://hub.sd2e.org/user/sd2e/design/YG_plasmid_024/1',
            'https://hub.sd2e.org/user/sd2e/design/YG_plasmid_022/1',
            'https://hub.sd2e.org/user/sd2e/design/YG_plasmid_023/1',
            'https://hub.sd2e.org/user/sd2e/design/YG_plasmid_002/1',
            'https://hub.sd2e.org/user/sd2e/design/pAN1201/1',
            'https://hub.sd2e.org/user/sd2e/design/YG_plasmid_025/1',
            'https://hub.sd2e.org/user/sd2e/design/pAN1717/1',
            'https://hub.sd2e.org/user/sd2e/design/pAN3928/1',
            'https://hub.sd2e.org/user/sd2e/design/pAN4036/1'
        }

        missing_plasmids = min_plasmids.difference(plasmids)

        assert len(missing_plasmids) == 0, "Failed to retrieve {num} of minimum {mini} plasmids from SD2 experiments. Missing: {miss}".format(num=repr(len(min_plasmids) - len(plasmids)), mini=repr(len(min_plasmids)), miss='\n'.join(missing_plasmids))

    def test_query_experiment_set_plasmids(self):
        sbh_query = SynBioHubQuery(SD2Constants.SD2_SERVER)
        sbh_query.login(self.user, self.password)

        plasmids = set(sbh_query.query_experiment_set_plasmids(SD2Constants.YEAST_GATES_EXPERIMENT_COLLECTION))

        min_plasmids = {
            'https://hub.sd2e.org/user/sd2e/design/YG_plasmid_021/1',
            'https://hub.sd2e.org/user/sd2e/design/YG_plasmid_010/1',
            'https://hub.sd2e.org/user/sd2e/design/YG_plasmid_003/1',
            'https://hub.sd2e.org/user/sd2e/design/YG_plasmid_015/1',
            'https://hub.sd2e.org/user/sd2e/design/YG_plasmid_001/1',
            'https://hub.sd2e.org/user/sd2e/design/YG_plasmid_014/1',
            'https://hub.sd2e.org/user/sd2e/design/YG_plasmid_017/1',
            'https://hub.sd2e.org/user/sd2e/design/YG_plasmid_005/1',
            'https://hub.sd2e.org/user/sd2e/design/YG_plasmid_018/1',
            'https://hub.sd2e.org/user/sd2e/design/YG_plasmid_008/1',
            'https://hub.sd2e.org/user/sd2e/design/YG_plasmid_020/1',
            'https://hub.sd2e.org/user/sd2e/design/YG_plasmid_012/1',
            'https://hub.sd2e.org/user/sd2e/design/YG_plasmid_004/1',
            'https://hub.sd2e.org/user/sd2e/design/YG_plasmid_019/1',
            'https://hub.sd2e.org/user/sd2e/design/YG_plasmid_009/1',
            'https://hub.sd2e.org/user/sd2e/design/YG_plasmid_006/1',
            'https://hub.sd2e.org/user/sd2e/design/YG_plasmid_011/1',
            'https://hub.sd2e.org/user/sd2e/design/YG_plasmid_016/1',
            'https://hub.sd2e.org/user/sd2e/design/YG_plasmid_007/1',
            'https://hub.sd2e.org/user/sd2e/design/YG_plasmid_024/1',
            'https://hub.sd2e.org/user/sd2e/design/YG_plasmid_022/1',
            'https://hub.sd2e.org/user/sd2e/design/YG_plasmid_023/1',
            'https://hub.sd2e.org/user/sd2e/design/YG_plasmid_002/1',
            'https://hub.sd2e.org/user/sd2e/design/YG_plasmid_025/1'
        }

        missing_plasmids = min_plasmids.difference(plasmids)

        assert len(missing_plasmids) == 0, "Failed to retrieve {num} of minimum {mini} plasmids from Yeast Gates experiments. Missing: {miss}".format(num=repr(len(min_plasmids) - len(plasmids)), mini=repr(len(min_plasmids)), miss='\n'.join(missing_plasmids))

    ############

    # def test_query_single_experiment_plasmids(self):
    #   yeast_gates_experiment = 'https://hub.sd2e.org/user/sd2e/experiment/biofab_yeast_gates_q0_aq_11269_4/1'

    #   sbh_query = SynBioHubQuery(SD2Constants.SD2_SERVER)
    #   plasmids = sbh_query.query_single_experiment_plasmids(yeast_gates_experiment)
    #   print(plasmids)

    # def test_query_sample_plasmids(self):
    #   rule_30_sample = 'https://hub.sd2e.org/user/sd2e/transcriptic_rule_30_q0_1_09242017/H07/1'

    #   sbh_query = SynBioHubQuery(SD2Constants.SD2_SERVER)
    #   plasmids = sbh_query.query_sample_plasmids(rule_30_sample)
    #   print(plasmids)

    # def test_query_condition_plasmids(self):
    #   rule_30_condition = 'https://hub.sd2e.org/user/sd2e/transcriptic_rule_30_q0_1_09242017/NEB_10_beta_pAN1717_Larabinose_5_aTc_0p002_IPTG_1_system/1'

    #   sbh_query = SynBioHubQuery(SD2Constants.SD2_SERVER)
    #   plasmids = sbh_query.query_condition_plasmids(rule_30_condition)
    #   print(plasmids)

    # # Test primer query methods \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

    def test_query_design_primers(self):
        downstream_gene = 'dnaA'

        sbh_query = SynBioHubQuery(SD2Constants.SD2_SERVER)
        sbh_query.login(self.user, self.password)

        primers = set(sbh_query.query_design_primers(with_sequence=False, pretty=True,
                                                     downstream_gene=downstream_gene))

        min_primers = {
            'https://hub.sd2e.org/user/sd2e/design/UCSB_PNNL_Output_Primer_4232/1',
            'https://hub.sd2e.org/user/sd2e/design/UCSB_PNNL_Output_Primer_4211/1',
            'https://hub.sd2e.org/user/sd2e/design/UCSB_PNNL_Output_Primer_3466/1',
            'https://hub.sd2e.org/user/sd2e/design/UCSB_PNNL_Output_Primer_11801/1',
            'https://hub.sd2e.org/user/sd2e/design/UCSB_PNNL_Output_Primer_2995/1',
            'https://hub.sd2e.org/user/sd2e/design/UCSB_PNNL_Output_Primer_0/1',
            'https://hub.sd2e.org/user/sd2e/design/UCSB_PNNL_Output_Primer_3417/1',
            'https://hub.sd2e.org/user/sd2e/design/UCSB_PNNL_Output_Primer_13595/1'
        }

        missing_primers = min_primers.difference(primers)

        assert len(missing_primers) == 0, "Failed to retrieve {num} of minimum {mini} primers with downstream gene {dg} from SD2 program. Missing: {miss}".format(num=repr(len(min_primers) - len(primers)), mini=repr(len(min_primers)), dg=downstream_gene, miss='\n'.join(missing_primers))

    def test_query_design_set_primers(self):
        downstream_gene = 'dnaA'

        sbh_query = SynBioHubQuery(SD2Constants.SD2_SERVER)
        sbh_query.login(self.user, self.password)

        primers = set(sbh_query.query_design_set_primers(SD2Constants.NOVEL_CHASSIS_DESIGN_COLLECTION,
                                                         with_sequence=False,
                                                         pretty=True,
                                                         downstream_gene=downstream_gene))

        min_primers = {
            'https://hub.sd2e.org/user/sd2e/design/UCSB_PNNL_Output_Primer_4232/1',
            'https://hub.sd2e.org/user/sd2e/design/UCSB_PNNL_Output_Primer_4211/1',
            'https://hub.sd2e.org/user/sd2e/design/UCSB_PNNL_Output_Primer_3466/1',
            'https://hub.sd2e.org/user/sd2e/design/UCSB_PNNL_Output_Primer_11801/1',
            'https://hub.sd2e.org/user/sd2e/design/UCSB_PNNL_Output_Primer_2995/1',
            'https://hub.sd2e.org/user/sd2e/design/UCSB_PNNL_Output_Primer_0/1',
            'https://hub.sd2e.org/user/sd2e/design/UCSB_PNNL_Output_Primer_3417/1',
            'https://hub.sd2e.org/user/sd2e/design/UCSB_PNNL_Output_Primer_13595/1'
        }

        missing_primers = min_primers.difference(primers)

        assert len(missing_primers) == 0, "Failed to retrieve {num} of minimum {mini} primers with downstream gene {dg} from Novel Chassis challenge problem. Missing: {miss}".format(num=repr(len(min_primers) - len(primers)), mini=repr(len(min_primers)), dg=downstream_gene, miss='\n'.join(missing_primers))

    # # Test riboswitch query methods \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

    def test_query_design_riboswitches(self):
        sbh_query = SynBioHubQuery(SD2Constants.SD2_SERVER)
        sbh_query.login(self.user, self.password)

        riboswitches = sbh_query.query_design_riboswitches(pretty=True)

        min_riboswitches = 193

        assert len(riboswitches) >= min_riboswitches, "Failed to retrieve {num} of minimum {mini} riboswitches from SD2 program.".format(num=repr(min_riboswitches - len(riboswitches)), mini=repr(min_riboswitches))

    def test_query_design_set_riboswitches(self):
        sbh_query = SynBioHubQuery(SD2Constants.SD2_SERVER)
        sbh_query.login(self.user, self.password)

        riboswitches = sbh_query.query_design_set_riboswitches(SD2Constants.RIBOSWITCHES_DESIGN_COLLECTION,
                                                               pretty=True)

        min_riboswitches = 193

        assert len(riboswitches) >= min_riboswitches, "Failed to retrieve {num} of minimum {mini} riboswitches from Riboswitches challenge problem.".format(num=repr(min_riboswitches - len(riboswitches)), mini=repr(min_riboswitches))

    # # Test strain query methods \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

    # def test_query_and_compare_strains(self):
    #   sbh_query = SynBioHubQuery(SD2Constants.SD2_SERVER)
    #   sbh_query.query_and_compare_strains(['https://hub.sd2e.org/user/sd2e/design/UWBF_7376/1', 'https://hub.sd2e.org/user/sd2e/design/UWBF_7375/1'])

    def test_query_design_strains(self):
        sbh_query = SynBioHubQuery(SD2Constants.SD2_SERVER)
        sbh_query.login(self.user, self.password)

        strains = sbh_query.query_design_strains(pretty=True)

        min_strains = 51

        msg = "Failed to retrieve {num} of minimum {mini} strains from SD2 program."
        assert len(strains) >= min_strains, msg.format(num=repr(min_strains - len(strains)),
                                                       mini=repr(min_strains))

    def test_query_design_set_strains(self):
        sbh_query = SynBioHubQuery(SD2Constants.SD2_SERVER)
        sbh_query.login(self.user, self.password)

        strains = set(sbh_query.query_design_set_strains(SD2Constants.YEAST_GATES_DESIGN_COLLECTION, pretty=True))

        min_strains = {
            'https://hub.sd2e.org/user/sd2e/design/UWBF_16967/1',
            'https://hub.sd2e.org/user/sd2e/design/UWBF_5783/1',
            'https://hub.sd2e.org/user/sd2e/design/UWBF_7300/1',
            'https://hub.sd2e.org/user/sd2e/design/UWBF_7374/1',
            'https://hub.sd2e.org/user/sd2e/design/UWBF_8542/1',
            'https://hub.sd2e.org/user/sd2e/design/UWBF_16970/1',
            'https://hub.sd2e.org/user/sd2e/design/UWBF_8544/1',
            'https://hub.sd2e.org/user/sd2e/design/UWBF_5993/1',
            'https://hub.sd2e.org/user/sd2e/design/UWBF_7373/1',
            'https://hub.sd2e.org/user/sd2e/design/UWBF_7376/1',
            'https://hub.sd2e.org/user/sd2e/design/UWBF_16969/1',
            'https://hub.sd2e.org/user/sd2e/design/W303/1',
            'https://hub.sd2e.org/user/sd2e/design/UWBF_5992/1',
            'https://hub.sd2e.org/user/sd2e/design/UWBF_6389/1',
            'https://hub.sd2e.org/user/sd2e/design/UWBF_6390/1',
            'https://hub.sd2e.org/user/sd2e/design/UWBF_6391/1',
            'https://hub.sd2e.org/user/sd2e/design/UWBF_8231/1',
            'https://hub.sd2e.org/user/sd2e/design/UWBF_8545/1',
            'https://hub.sd2e.org/user/sd2e/design/UWBF_6388/1',
            'https://hub.sd2e.org/user/sd2e/design/UWBF_7299/1',
            'https://hub.sd2e.org/user/sd2e/design/UWBF_7375/1',
            'https://hub.sd2e.org/user/sd2e/design/UWBF_7377/1',
            'https://hub.sd2e.org/user/sd2e/design/UWBF_8225/1',
            'https://hub.sd2e.org/user/sd2e/design/UWBF_8543/1',
            'https://hub.sd2e.org/user/sd2e/design/UWBF_16968/1'
        }

        missing_strains = min_strains.difference(strains)

        assert len(missing_strains) == 0, "Failed to retrieve {num} of minimum {mini} strains from Yeast Gates challenge problem. Missing: {miss}".format(num=repr(len(min_strains) - len(strains)), mini=repr(len(min_strains)), miss='\n'.join(missing_strains))

    def test_query_experiment_strains(self):
        sbh_query = SynBioHubQuery(SD2Constants.SD2_SERVER)
        sbh_query.login(self.user, self.password)

        strains = set(sbh_query.query_experiment_strains())

        min_strains = {
            'https://hub.sd2e.org/user/sd2e/design/UWBF_16967/1',
            'https://hub.sd2e.org/user/sd2e/design/UWBF_5783/1',
            'https://hub.sd2e.org/user/sd2e/design/UWBF_7300/1',
            'https://hub.sd2e.org/user/sd2e/design/UWBF_7374/1',
            'https://hub.sd2e.org/user/sd2e/design/UWBF_8542/1',
            'https://hub.sd2e.org/user/sd2e/design/UWBF_16970/1',
            'https://hub.sd2e.org/user/sd2e/design/UWBF_8544/1',
            'https://hub.sd2e.org/user/sd2e/design/UWBF_5993/1',
            'https://hub.sd2e.org/user/sd2e/design/UWBF_7373/1',
            'https://hub.sd2e.org/user/sd2e/design/UWBF_7376/1',
            'https://hub.sd2e.org/user/sd2e/design/UWBF_16969/1',
            'https://hub.sd2e.org/user/sd2e/design/UWBF_5992/1',
            'https://hub.sd2e.org/user/sd2e/design/UWBF_6389/1',
            'https://hub.sd2e.org/user/sd2e/design/UWBF_6390/1',
            'https://hub.sd2e.org/user/sd2e/design/UWBF_6391/1',
            'https://hub.sd2e.org/user/sd2e/design/UWBF_8231/1',
            'https://hub.sd2e.org/user/sd2e/design/UWBF_8545/1',
            'https://hub.sd2e.org/user/sd2e/design/UWBF_6388/1',
            'https://hub.sd2e.org/user/sd2e/design/UWBF_7299/1',
            'https://hub.sd2e.org/user/sd2e/design/UWBF_7375/1',
            'https://hub.sd2e.org/user/sd2e/design/UWBF_7377/1',
            'https://hub.sd2e.org/user/sd2e/design/UWBF_8225/1',
            'https://hub.sd2e.org/user/sd2e/design/UWBF_8543/1',
            'https://hub.sd2e.org/user/sd2e/design/UWBF_16968/1'
        }

        missing_strains = min_strains.difference(strains)

        assert len(missing_strains) == 0, "Failed to retrieve {num} of minimum {mini} strains from SD2 experiments. Missing: {miss}".format(num=repr(len(min_strains) - len(strains)), mini=repr(len(min_strains)), miss='\n'.join(missing_strains))

    def test_query_experiment_set_strains(self):
        sbh_query = SynBioHubQuery(SD2Constants.SD2_SERVER)
        sbh_query.login(self.user, self.password)

        strains = set(sbh_query.query_experiment_set_strains(SD2Constants.YEAST_GATES_EXPERIMENT_COLLECTION))

        min_strains = {
            'https://hub.sd2e.org/user/sd2e/design/UWBF_5783/1',
            'https://hub.sd2e.org/user/sd2e/design/UWBF_5993/1',
            'https://hub.sd2e.org/user/sd2e/design/UWBF_5992/1',
            'https://hub.sd2e.org/user/sd2e/design/UWBF_8225/1',
            'https://hub.sd2e.org/user/sd2e/design/UWBF_6389/1',
            'https://hub.sd2e.org/user/sd2e/design/UWBF_6390/1',
            'https://hub.sd2e.org/user/sd2e/design/UWBF_6391/1',
            'https://hub.sd2e.org/user/sd2e/design/UWBF_6388/1',
            'https://hub.sd2e.org/user/sd2e/design/UWBF_7374/1',
            'https://hub.sd2e.org/user/sd2e/design/UWBF_7373/1',
            'https://hub.sd2e.org/user/sd2e/design/UWBF_7376/1',
            'https://hub.sd2e.org/user/sd2e/design/UWBF_7375/1',
            'https://hub.sd2e.org/user/sd2e/design/UWBF_8542/1',
            'https://hub.sd2e.org/user/sd2e/design/UWBF_8544/1',
            'https://hub.sd2e.org/user/sd2e/design/UWBF_8545/1',
            'https://hub.sd2e.org/user/sd2e/design/UWBF_8543/1',
            'https://hub.sd2e.org/user/sd2e/design/UWBF_16967/1',
            'https://hub.sd2e.org/user/sd2e/design/UWBF_16970/1',
            'https://hub.sd2e.org/user/sd2e/design/UWBF_16969/1',
            'https://hub.sd2e.org/user/sd2e/design/UWBF_16968/1',
            'https://hub.sd2e.org/user/sd2e/design/UWBF_7300/1',
            'https://hub.sd2e.org/user/sd2e/design/UWBF_8231/1',
            'https://hub.sd2e.org/user/sd2e/design/UWBF_7299/1',
            'https://hub.sd2e.org/user/sd2e/design/UWBF_7377/1'
        }

        missing_strains = min_strains.difference(strains)

        assert len(missing_strains) == 0, "Failed to retrieve {num} of minimum {mini} strains from Yeast Gates experiments. Missing: {miss}".format(num=repr(len(min_strains) - len(strains)), mini=repr(len(min_strains)), miss='\n'.join(missing_strains))

    # def test_query_single_experiment_strains(self):
    #   rule_30_experiment = 'https://hub.sd2e.org/user/sd2e/experiment/transcriptic_rule_30_q0_1_09242017/1'

    #   sbh_query = SynBioHubQuery(SD2Constants.SD2_SERVER)
    #   strains = sbh_query.query_single_experiment_strains(rule_30_experiment)
    #   print(strains)

    # # Test sample query methods \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

    # def test_query_single_experiment_samples_by_probability(self):
    #   yeast_gates_experiment = 'https://hub.sd2e.org/user/sd2e/experiment/biofab_yeast_gates_q0_aq_10843/1'

    #   sbh_query = SynBioHubQuery(SD2Constants.SD2_SERVER)
    #   samples = sbh_query.query_single_experiment_samples_by_probability(yeast_gates_experiment, 0.4)
    #   print(samples)

    # # Test experiment data query methods \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

    # def test_query_single_experiment_data(self):
    #   yeast_gates_experiment = 'https://hub.sd2e.org/user/sd2e/experiment/biofab_yeast_gates_q0_aq_10843/1'

    #   sbh_query = SynBioHubQuery(SD2Constants.SD2_SERVER)
    #   exp_data = sbh_query.query_single_experiment_data(yeast_gates_experiment)
    #   print(exp_data)

    # # Test experiment intent query methods \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

    # def test_query_single_experiment_intent(self):
    #   yeast_gates_experiment = 'https://hub.sd2e.org/user/sd2e/experiment/biofab_yeast_gates_q0_aq_12548_3/1'

    #   sbh_query = SynBioHubQuery(SD2Constants.SD2_SERVER)
    #   exp_intent = sbh_query.query_single_experiment_intent(yeast_gates_experiment)
    #   print(exp_intent)

    # # Test design and experiment set query methods \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

    def test_query_design_sets(self):
        sbh_query = SynBioHubQuery(SD2Constants.SD2_SERVER)
        sbh_query.login(self.user, self.password)

        design_sets = set(sbh_query.query_design_sets(pretty=True))

        min_design_sets = {
            'https://hub.sd2e.org/user/sd2e/design/yeast_gates/1',
            'https://hub.sd2e.org/user/sd2e/design/yeast_gates_plasmids/1',
            'https://hub.sd2e.org/user/sd2e/design/yeast_gates_strains/1',
            'https://hub.sd2e.org/user/sd2e/design/novel_chassis_genomes/1',
            'https://hub.sd2e.org/user/sd2e/design/novel_chassis_primers/1',
            'https://hub.sd2e.org/user/sd2e/design/Riboswitches/1',
            'https://hub.sd2e.org/user/sd2e/design/novel_chassis/1',
            'https://hub.sd2e.org/user/sd2e/design/novel_chassis_strains/1',
            'https://hub.sd2e.org/user/sd2e/design/rule_30/1',
            'https://hub.sd2e.org/user/sd2e/design/SBME_Cell_Free/1'
        }

        missing_design_sets = min_design_sets.difference(design_sets)

        assert len(missing_design_sets) == 0, "Failed to retrieve {num} of minimum {mini} design collections from SD2 program. Missing: {miss}".format(num=repr(len(min_design_sets) - len(design_sets)), mini=repr(len(min_design_sets)), miss='\n'.join(missing_design_sets))

    def test_query_experiment_sets(self):
        sbh_query = SynBioHubQuery(SD2Constants.SD2_SERVER)
        sbh_query.login(self.user, self.password)

        exp_sets = set(sbh_query.query_experiment_sets())

        min_exp_sets = {
            'https://hub.sd2e.org/user/sd2e/experiment/transcriptic_yeast_gates/1',
            'https://hub.sd2e.org/user/sd2e/experiment/rule_30/1',
            'https://hub.sd2e.org/user/sd2e/experiment/biofab_yeast_gates/1',
            'https://hub.sd2e.org/user/sd2e/experiment/yeast_gates/1'
        }

        missing_exp_sets = min_exp_sets.difference(exp_sets)

        assert len(missing_exp_sets) == 0, "Failed to retrieve {num} of minimum {mini} experiment collections from SD2 program. Missing: {miss}".format(num=repr(len(min_exp_sets) - len(exp_sets)), mini=repr(len(min_exp_sets)), miss='\n'.join(missing_exp_sets))

    def test_query_experiment_set_size(self):
        experiment_set = SD2Constants.YEAST_GATES_EXPERIMENT_COLLECTION

        sbh_query = SynBioHubQuery(SD2Constants.SD2_SERVER)
        sbh_query.login(self.user, self.password)

        exp_set_size = sbh_query.query_experiment_set_size(experiment_set)

        min_exp_set_size = 46

        assert exp_set_size >= min_exp_set_size, "Failed to retrieve {num} of minimum {mini} experiments from collection with URI <{es}>.".format(num=repr(min_exp_set_size - exp_set_size), mini=repr(min_exp_set_size), es=experiment_set)

    # # Test attachment retrieval methods \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

    # def test_query_plan_attachments(self):
    #   sbh_query = SynBioHubQuery(SD2Constants.SD2_SERVER)
    #   plan_attachments = sbh_query.query_single_experiment_attachments("https://hub.sd2e.org/user/sd2e/experiment/biofab_yeast_gates_q0_aq_11269_1/1")
    #   assert plan_attachments is not None and len(plan_attachments['results']['bindings']) == 1
    #   print(plan_attachments)

    #   plan_attachments = sbh_query.query_single_experiment_attachments("foo")
    #   assert plan_attachments is not None and len(plan_attachments['results']['bindings']) == 0
    #   print(plan_attachments)

    # def test_query_plan_named_attachments(self):
    #   sbh_query = SynBioHubQuery(SD2Constants.SD2_SERVER)
    #   plan_attachments = sbh_query.query_single_experiment_attachment("https://hub.sd2e.org/user/sd2e/experiment/biofab_yeast_gates_q0_intent_control_test/1", "biofab_yg_UWBF_NOR_intent_control_test.json")
    #   assert plan_attachments is not None and len(plan_attachments['results']['bindings']) == 1
    #   print(plan_attachments)

    #   plan_attachments = sbh_query.query_single_experiment_attachment("https://hub.sd2e.org/user/sd2e/experiment/biofab_yeast_gates_q0_intent_control_test/1", "biofab_yg_UWBF_NOR_intent_control_test_sample_attributes.json")
    #   assert plan_attachments is not None and len(plan_attachments['results']['bindings']) == 1
    #   print(plan_attachments)

    #   plan_attachments = sbh_query.query_single_experiment_attachment("https://hub.sd2e.org/user/sd2e/experiment/biofab_yeast_gates_q0_intent_control_test/1", "foo")
    #   assert plan_attachments is not None and len(plan_attachments['results']['bindings']) == 0
    #   print(plan_attachments)

    # # Test lab query methods \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

    def test_query_designs_by_lab_ids(self):
        sbh_query = SynBioHubQuery(SD2Constants.SD2_SERVER)
        sbh_query.login(self.user, self.password)

        designs = sbh_query.query_designs_by_lab_ids(SD2Constants.GINKGO, ['1'], verbose=True)
        expected_designs = {'1': {'identity': 'https://hub.sd2e.org/user/sd2e/design/CAT_G33_500/1',
                                  'name': 'Glycerol'}}
        assert expected_designs == designs

        designs = sbh_query.query_designs_by_lab_ids(SD2Constants.CALTECH, ['a'], verbose=True)
        expected_designs = {'a': {'identity': 'https://hub.sd2e.org/user/sd2e/design/Murray0x20BioCon0x20A/1',
                                  'name': 'Murray BioCon A'}}
        assert expected_designs == designs

    def test_query_lab_ids_by_designs(self):
        sbh_query = SynBioHubQuery(SD2Constants.SD2_SERVER)
        sbh_query.login(self.user, self.password)
        # Test with default options
        lab_ids = sbh_query.query_lab_ids_by_designs(SD2Constants.GINKGO,
                                                     ['https://hub.sd2e.org/user/sd2e/design/CAT_G33_500/1'])
        expected = {'https://hub.sd2e.org/user/sd2e/design/CAT_G33_500/1': '1'}
        assert expected == lab_ids
        # Test with verbose (default is False)
        lab_ids = sbh_query.query_lab_ids_by_designs(SD2Constants.GINKGO,
                                                     ['https://hub.sd2e.org/user/sd2e/design/CAT_G33_500/1'],
                                                     verbose=True)
        expected = {'https://hub.sd2e.org/user/sd2e/design/CAT_G33_500/1': {'id': '1',
                                                                            'name': 'Glycerol'}}
        assert expected == lab_ids
        # Test without pretty (default is True)
        lab_ids = sbh_query.query_lab_ids_by_designs(SD2Constants.GINKGO,
                                                     ['https://hub.sd2e.org/user/sd2e/design/CAT_G33_500/1'],
                                                     pretty=False)
        expected = {'head': {'link': [],
                             'vars': ['design', 'name', 'id']},
                    'results': {'distinct': False,
                                'ordered': True,
                                'bindings': [{'design':
                                              {'type': 'uri',
                                               'value': 'https://hub.sd2e.org/user/sd2e/design/CAT_G33_500/1'},
                                              'name': {'type': 'literal',
                                                       'value': 'Glycerol'},
                                              'id': {'type': 'literal',
                                                     'value': '1'}}]}}
        assert expected == lab_ids
        # Test querying multiple designs
        designs = ['https://hub.sd2e.org/user/sd2e/design/UWBF_6390/1',
                   'https://hub.sd2e.org/user/sd2e/design/CAT_G33_500/1']
        lab_ids = sbh_query.query_lab_ids_by_designs(SD2Constants.GINKGO,
                                                     designs)
        expected = {'https://hub.sd2e.org/user/sd2e/design/CAT_G33_500/1': '1',
                    'https://hub.sd2e.org/user/sd2e/design/UWBF_6390/1': '162063'}
        assert expected == lab_ids

    # Test statistics query methods \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

    # def test_query_synbiohub_statistics(self):
    #   sbh_query = SynBioHubQuery(SD2Constants.SD2_SERVER)
    #   sbh_query.query_synbiohub_statistics()

    # Note: This BBN instance will successfully query infomration if the user is directly connected to BBN's server
    # def test_bbnSBH(self):
    #   server = SD2Constants.BBN_SERVER
    #   collection = SD2Constants.BBN_RULE30_COLLECTION
    #   sbhQuery = SynBioHubQuery(server)
    #   sample = sbhQuery.query_experiment_plasmids(collection)
    #   print('Successfully Queried BBN instance!')


if __name__ == '__main__':
    unittest.main()
