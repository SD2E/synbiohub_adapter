import getpass
import os
import unittest

import synbiohub_adapter as sbha


class TestStyle(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.user = 'sd2e'
        if 'SBH_PASSWORD' in os.environ.keys():
            self.password = os.environ['SBH_PASSWORD']
        else:
            self.password = getpass.getpass()
        # Use the staging server so we don't bother the production server
        self.sbol_query = sbha.SBOLQuery(sbha.SD2Constants.SD2_STAGING_SERVER,
                                         spoofed_url=sbha.SD2Constants.SD2_SERVER)
        self.sbol_query.login(self.user, self.password)

    def test_serialize_options(self):
        # pairs of input and expected results
        cases = [
            ([], ''),
            (['alpha'], '( <alpha> )'),
            (['alpha', 'beta'], '( <alpha> ) ( <beta> )'),
            ('alpha', '( <alpha> )')
        ]
        for arg, expected in cases:
            self.assertEqual(self.sbol_query.serialize_options(arg), expected)
        with self.assertRaises(TypeError) as _:
            self.sbol_query.serialize_options(None)

    def test_serialize_literal_options(self):
        # pairs of input and expected results
        cases = [
            ([], ''),
            (['alpha'], '( "alpha" )'),
            (['alpha', 'beta'], '( "alpha" ) ( "beta" )'),
            ('alpha', '( "alpha" )')
        ]
        for arg, expected in cases:
            self.assertEqual(self.sbol_query.serialize_literal_options(arg), expected)
        with self.assertRaises(TypeError) as _:
            self.sbol_query.serialize_literal_options(None)

    def test_serialize_objects(self):
        # pairs of input and expected results
        cases = [
            ([], ''),
            (['alpha'], '<alpha>'),
            (['alpha', 'beta'], '<alpha>, <beta>'),
            ('alpha', '<alpha>')
        ]
        for arg, expected in cases:
            self.assertEqual(self.sbol_query.serialize_objects(arg), expected)
        with self.assertRaises(TypeError) as _:
            self.sbol_query.serialize_objects(None)

    def test_query_collections(self):
        collections = self.sbol_query.query_collections([sbha.SD2Constants.YEAST_GATES_DESIGN_COLLECTION])
        collections2 = self.sbol_query.query_collections(sbha.SD2Constants.YEAST_GATES_DESIGN_COLLECTION)
        self.assertEqual(collections, collections2)
