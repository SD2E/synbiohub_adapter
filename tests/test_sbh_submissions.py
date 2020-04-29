import unittest

from synbiohub_adapter.upload_sbol.upload_sbol import SynBioHub
from synbiohub_adapter.SynBioHubUtil import SD2Constants
import sbol
from getpass import getpass
import os


class TestSBHSubmissions(unittest.TestCase):
    '''
        This class will perform unit testing to submit SBOL data to SynBioHub.

        To run this python file, enter in the following command from the synbiohub_adapter directory:
            python -m unittest tests/test_sbh_submissions.py
    '''

    @classmethod
    def setUpClass(self):
        self.user = 'sd2e'
        if 'SBH_PASSWORD' in os.environ.keys():
            self.password = os.environ['SBH_PASSWORD']
        else:
            self.password = getpass()

    def test_submit_collection(self):

        sbh = SynBioHub(SD2Constants.SD2_STAGING_SERVER, self.user, self.password,
                        SD2Constants.SD2_STAGING_SERVER + '/sparql', SD2Constants.SD2_SERVER)

        sbol.Config.setOption('sbol_typed_uris', False)
        sbol.Config.setOption('validate', False)
        sbol.setHomespace('http://dummy.org')

        member_ID = 'foo'

        doc = sbol.Document()
        doc.componentDefinitions.create(member_ID)

        collection_ID = 'adapter_test_1'
        collection_name = 'Adapter Test Collection 1'
        collection_description = 'This is a test of the upload_sbol module of synbiohub_adapter.'
        collection_version = '1'

        sbh.submit_collection(doc, collection_ID, collection_version, collection_name,
                              collection_description, overwrite=True)

        member_identity = '/'.join([SD2Constants.SD2_SERVER, 'user', self.user, collection_ID,
                                    member_ID, '1'])
        collection_identity = '/'.join([SD2Constants.SD2_SERVER, 'user', self.user, collection_ID,
                                        collection_ID + '_collection', '1'])

        query_result = sbh.query_collection_members(collection_uris=[collection_identity])

        self.assertIn(collection_identity, query_result)
        self.assertEqual(len(query_result[collection_identity]), 1)
        self.assertIn(member_identity, query_result[collection_identity])

    def test_submit_sub_collection(self):
        sbh = SynBioHub(SD2Constants.SD2_STAGING_SERVER, self.user, self.password,
                        SD2Constants.SD2_STAGING_SERVER + '/sparql', SD2Constants.SD2_SERVER)

        sbol.Config.setOption('sbol_typed_uris', False)
        sbol.Config.setOption('validate', False)
        sbol.setHomespace('http://dummy.org')

        doc = sbol.Document()

        collection_ID = 'adapter_test_2'
        collection_name = 'Adapter Test Collection 2'
        collection_description = 'This is a test of the upload_sbol module of synbiohub_adapter.'
        collection_version = '1'

        sub_collection_ID = 'sub_adapter_test'
        sub_collection_name = 'Sub Adapter Test Collection'
        sub_collection_description = 'This is a test of the upload_sbol module of synbiohub_adapter.'
        sub_collection_version = '1'

        sbh.submit_collection(doc, collection_ID, collection_version, collection_name,
                              collection_description, 0, sub_collection_ID, sub_collection_version,
                              sub_collection_name, sub_collection_description, overwrite=True)

        collection_identity = '/'.join([SD2Constants.SD2_SERVER, 'user', self.user, collection_ID,
                                        collection_ID + '_collection', '1'])
        sub_collection_identity = '/'.join([SD2Constants.SD2_SERVER, 'user', self.user, collection_ID,
                                            sub_collection_ID, '1'])

        query_result = sbh.query_collection_members(collection_uris=[collection_identity])

        self.assertIn(collection_identity, query_result)
        self.assertEqual(len(query_result[collection_identity]), 1)
        self.assertIn(sub_collection_identity, query_result[collection_identity])

    def test_submit_to_collection(self):
        sbh = SynBioHub(SD2Constants.SD2_STAGING_SERVER, self.user, self.password,
                        SD2Constants.SD2_STAGING_SERVER + '/sparql', SD2Constants.SD2_SERVER)

        sbol.Config.setOption('sbol_typed_uris', False)
        sbol.Config.setOption('validate', False)
        sbol.setHomespace('http://dummy.org')

        member_ID1 = 'foo'

        doc1 = sbol.Document()
        doc1.componentDefinitions.create(member_ID1)

        collection_ID = 'adapter_test_3'
        collection_name = 'Adapter Test Collection 3'
        collection_description = 'This is a test of the upload_sbol module of synbiohub_adapter.'
        collection_version = '1'

        sbh.submit_collection(doc1, collection_ID, collection_version, collection_name,
                              collection_description, overwrite=True)

        member_identity1 = '/'.join([SD2Constants.SD2_SERVER, 'user', self.user, collection_ID,
                                     member_ID1, '1'])
        collection_identity = '/'.join([SD2Constants.SD2_SERVER, 'user', self.user, collection_ID,
                                        collection_ID + '_collection', '1'])

        member_ID2 = 'bar'

        doc2 = sbol.Document()
        doc2.componentDefinitions.create(member_ID2)

        sbh.submit_to_collection([doc2], collection_identity)

        member_identity2 = '/'.join([SD2Constants.SD2_SERVER, 'user', self.user, collection_ID,
                                     member_ID2, '1'])

        query_result = sbh.query_collection_members(collection_uris=[collection_identity])

        self.assertIn(collection_identity, query_result)
        self.assertEqual(len(query_result[collection_identity]), 2)
        self.assertIn(member_identity1, query_result[collection_identity])
        self.assertIn(member_identity2, query_result[collection_identity])

    @unittest.expectedFailure
    def test_submit_to_sub_collection(self):
        sbh = SynBioHub(SD2Constants.SD2_STAGING_SERVER, self.user, self.password,
                        SD2Constants.SD2_STAGING_SERVER + '/sparql', SD2Constants.SD2_SERVER)

        sbol.Config.setOption('sbol_typed_uris', False)
        sbol.Config.setOption('validate', False)
        sbol.setHomespace('http://dummy.org')

        doc1 = sbol.Document()

        collection_ID = 'adapter_test_4'
        collection_name = 'Adapter Test Collection 4'
        collection_description = 'This is a test of the upload_sbol module of synbiohub_adapter.'
        collection_version = '1'

        sub_collection_ID = 'sub_adapter_test'
        sub_collection_name = 'Sub Adapter Test Collection'
        sub_collection_description = 'This is a test of the upload_sbol module of synbiohub_adapter.'
        sub_collection_version = '1'

        sbh.submit_collection(doc1, collection_ID, collection_version, collection_name,
                              collection_description, 0, sub_collection_ID, sub_collection_version,
                              sub_collection_name, sub_collection_description, overwrite=True)

        collection_identity = '/'.join([SD2Constants.SD2_SERVER, 'user', self.user, collection_ID,
                                        collection_ID + '_collection', '1'])
        sub_collection_identity = '/'.join([SD2Constants.SD2_SERVER, 'user', self.user, collection_ID,
                                            sub_collection_ID, '1'])

        member_ID1 = 'bar'

        doc2 = sbol.Document()
        doc2.componentDefinitions.create(member_ID1)

        sbh.submit_to_collection([doc2], collection_identity, overwrite=True, sub_collection_id=sub_collection_ID,
                                 sub_collection_version=sub_collection_version,
                                 sub_collection_name=sub_collection_name,
                                 sub_collection_description=sub_collection_description)

        member_identity1 = '/'.join([SD2Constants.SD2_SERVER, 'user', self.user, collection_ID,
                                     member_ID1, '1'])

        member_ID2 = 'foo'

        doc3 = sbol.Document()
        doc3.componentDefinitions.create(member_ID2)

        sbh.submit_to_collection([doc3], collection_identity, overwrite=True, sub_collection_id=sub_collection_ID,
                                 sub_collection_version=sub_collection_version,
                                 sub_collection_name=sub_collection_name,
                                 sub_collection_description=sub_collection_description)

        member_identity2 = '/'.join([SD2Constants.SD2_SERVER, 'user', self.user, collection_ID,
                                     member_ID2, '1'])

        query_result1 = sbh.query_collection_members(collection_uris=[collection_identity])

        self.assertEqual(len(query_result1[collection_identity]), 3)
        self.assertIn(member_identity1, query_result1[collection_identity])
        self.assertIn(member_identity2, query_result1[collection_identity])
        self.assertIn(sub_collection_identity, query_result1[collection_identity])

        query_result2 = sbh.query_collection_members(collection_uris=[sub_collection_identity])

        self.assertEqual(len(query_result2[sub_collection_identity]), 2)
        self.assertIn(member_identity1, query_result2[sub_collection_identity])
        self.assertIn(member_identity2, query_result2[sub_collection_identity])


if __name__ == '__main__':
    unittest.main()
