# coding=utf-8
import unittest2 as unittest

from redomino.revision.testing import REDOMINO_REVISION_INTEGRATION_TESTING


class TestRevisionFile(unittest.TestCase):
    layer = REDOMINO_REVISION_INTEGRATION_TESTING

    def _revision1(self):
        portal = self.layer['portal']

        return portal['revision1']

    def _revision2(self):
        portal = self.layer['portal']

        return portal['revision2']

    def _revisionfile11_info(self):
        from redomino.revision.interfaces import IRevisionFileInfo
        portal = self.layer['portal']

        revision11 = portal['revision1']['1']
        return IRevisionFileInfo(revision11)

    def _revisionfile12_info(self):
        from redomino.revision.interfaces import IRevisionFileInfo
        portal = self.layer['portal']

        revision12 = portal['revision1']['2']
        return IRevisionFileInfo(revision12)

    def _revisionfile21_info(self):
        from redomino.revision.interfaces import IRevisionFileInfo
        portal = self.layer['portal']

        revision21 = portal['revision2']['1']
        return IRevisionFileInfo(revision21)

    def test_revisionfile_info_adapter(self):
        """ """
        from redomino.revision.interfaces import IRevisionFileInfo
        revisionfile11_info = self._revisionfile11_info()
        self.assertTrue(IRevisionFileInfo.providedBy(revisionfile11_info))
        from redomino.revision.content.revisionfile import RevisionFileInfo
        self.assertIsInstance(revisionfile11_info, RevisionFileInfo)

        self.assertTrue(IRevisionFileInfo.implementedBy(RevisionFileInfo))

    def test_code(self):
        """ The revision file code """
        revisionfile11_info = self._revisionfile11_info()
        self.assertEquals('1', revisionfile11_info.code())

    def test_parent_code(self):
        """ The parent revision file code """
        revisionfile11_info = self._revisionfile11_info()
        self.assertEquals('revision1', revisionfile11_info.parent_code())

    def test_title(self):
        """ The revision file title """
        revisionfile11_info = self._revisionfile11_info()
        self.assertEquals('1', revisionfile11_info.title())

    def test_description(self):
        """ The revision file description """
        revisionfile11_info = self._revisionfile11_info()
        self.assertEquals('1', revisionfile11_info.description())

    def test_keywords(self):
        """ The revision keywords """
        revisionfile11_info = self._revisionfile11_info()
        self.assertEquals(('keyword1',), revisionfile11_info.keywords())

    def test_creation_date(self):
        """ Creation date """
        revisionfile11_info = self._revisionfile11_info()

        from DateTime import DateTime
        self.assertTrue(revisionfile11_info.creation_date(), DateTime)

    def test_publication_date(self):
        """ Publication date"""
        revisionfile11_info = self._revisionfile11_info()

        from DateTime import DateTime
        self.assertTrue(revisionfile11_info.publication_date(), DateTime)

    def test_referring(self):
        """ Other revision files (IRevisionFile) related by this document """
        revisionfile11_info = self._revisionfile11_info()
        self.assertEquals(1, len(revisionfile11_info.referring()))

    def test_referring_info(self):
        """ Other revision files info (IRevisionFile) related by this document """
        revisionfile11_info = self._revisionfile11_info()
        self.assertEquals(1, len(revisionfile11_info.referring_info()))

    def test_referred_by(self):
        """ Other revision files (IRevisionFile) that refer this document """
        revisionfile11_info = self._revisionfile11_info()
        self.assertEquals(1, len(revisionfile11_info.referring()))

    def test_referred_by_info(self):
        """ Other revision files info (IRevisionFile) that refer this document """
        revisionfile11_info = self._revisionfile11_info()
        self.assertEquals(1, len(revisionfile11_info.referred_by_info()))

    def test_url11(self):
        """ The view url """
        revision1 = self._revision1()
        revisionfile11_info = self._revisionfile11_info()
        self.assertEquals('%s/view' % revision1['1'].absolute_url(), revisionfile11_info.url())

    def test_url21(self):
        """ The view url """
        revision2 = self._revision2()
        revisionfile21_info = self._revisionfile21_info()
        self.assertEquals('%s' % revision2['1'].absolute_url(), revisionfile21_info.url())

    def test_download_url11(self):
        """ The download url, if applicable """
        revision1 = self._revision1()
        revisionfile11_info = self._revisionfile11_info()
        self.assertEquals(revision1['1'].absolute_url(), revisionfile11_info.download_url())

    def test_download_url21(self):
        """ The download url, if applicable """
        revisionfile21_info = self._revisionfile21_info()
        self.assertFalse(revisionfile21_info.download_url())

    def test_status11(self):
        """ The revisionfile status """
        revision1 = self._revision1()
        revision11 = revision1['1']
        revisionfile11_info = self._revisionfile11_info()
        portal_workflow = self.layer['portal'].portal_workflow
        self.assertEquals(portal_workflow.getInfoFor(revision11, 'review_state'), revisionfile11_info.status())

    def test_revision_folder(self):
        """ Returns the revision folder """
        revision1 = self._revision1()
        revisionfile11_info = self._revisionfile11_info()
        self.assertEquals(revision1, revisionfile11_info.revision_folder())

    def test_is_latest(self):
        """ Is the latest revision? """
        revisionfile11_info = self._revisionfile11_info()
        revisionfile12_info = self._revisionfile12_info()

        self.assertFalse(revisionfile11_info.is_latest())
        self.assertTrue(revisionfile12_info.is_latest())

    def test_base_url(self):
        """ The base url (absolute_url) """
        revision1 = self._revision1()
        revisionfile11_info = self._revisionfile11_info()
        self.assertEquals(revision1['1'].absolute_url(), revisionfile11_info.base_url())






