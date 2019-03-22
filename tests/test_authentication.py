import os
import unittest

import synbiohub_adapter as sbha
import SPARQLWrapper


class TestAuthentication(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.user = 'sd2e'
        if 'SBH_PASSWORD' in os.environ.keys():
            self.password = os.environ['SBH_PASSWORD']
        else:
            self.password = getpass()

    def test_login(self):
        sbh_query = sbha.SynBioHubQuery(sbha.SD2Constants.SD2_SERVER)
        result = sbh_query.login(self.user, self.password)
        self.assertEqual(result, None)

    def test_wrong_password(self):
        sbh_query = sbha.SynBioHubQuery(sbha.SD2Constants.SD2_SERVER)
        with self.assertRaises(SPARQLWrapper.SPARQLExceptions.Unauthorized) as exc:
            sbh_query.login(self.user, 'Not_the_PaSsW0rD')

    def test_wrong_user(self):
        sbh_query = sbha.SynBioHubQuery(sbha.SD2Constants.SD2_SERVER)
        with self.assertRaises(SPARQLWrapper.SPARQLExceptions.Unauthorized) as exc:
            sbh_query.login('Not_the_U5eR', self.password)
