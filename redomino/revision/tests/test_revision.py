# coding=utf-8
import unittest2 as unittest

from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles

from redomino.revision.testing import REDOMINO_REVISION_INTEGRATION_TESTING
from redomino.revision.testing import REDOMINO_REVISION_INTEGRATION_TESTING1
from redomino.revision.testing import REDOMINO_REVISION_INTEGRATION_TESTING2
from redomino.revision.testing import REDOMINO_REVISION_INTEGRATION_TESTING3
from redomino.revision.testing import REDOMINO_REVISION_INTEGRATION_TESTING4


class TestRevisionFileMixin():

    def _revision1(self):
        portal = self.layer['portal']

        return portal['revision1']

    def _revision1_info(self):
        from redomino.revision.interfaces import IRevisionInfo
        portal = self.layer['portal']

        revision1 = portal['revision1']
        return IRevisionInfo(revision1)


class TestRevisionFile(TestRevisionFileMixin, unittest.TestCase):
    layer = REDOMINO_REVISION_INTEGRATION_TESTING

    def test_revision_info_adapter(self):
        """ """
        from redomino.revision.interfaces import IRevisionInfo
        revision1_info = self._revision1_info()
        self.assertTrue(IRevisionInfo.providedBy(revision1_info))
        from redomino.revision.content.revision import RevisionInfo
        self.assertIsInstance(revision1_info, RevisionInfo)

        self.assertTrue(IRevisionInfo.implementedBy(RevisionInfo))

    def test_code(self):
        """ The revision code """
        revision1_info = self._revision1_info()
        self.assertEquals('revision1', revision1_info.code())

    def test_title(self):
        """ The revision title """
        revision1_info = self._revision1_info()
        self.assertEquals('title', revision1_info.title())

    def test_description(self):
        """ The revision description """
        revision1_info = self._revision1_info()
        self.assertEquals('description', revision1_info.description())

    def test_latest(self):
        """ The latest revision """
        portal = self.layer['portal']
        revision1_info = self._revision1_info()
        self.assertEquals(revision1_info.latest(), portal['revision1']['2'])

    def test_latest_info(self):
        """ The latest revision info """
        portal = self.layer['portal']
        revision1_info = self._revision1_info()
        self.assertEquals(revision1_info.latest_info()['url'], '%s/view' % portal['revision1']['2'].absolute_url())

    def test_revisionfiles(self):
        """ All the revision files, ordered """
        revision1 = self._revision1()
        revision1_info = self._revision1_info()
        from redomino.revision.interfaces import IRevisionFile
        self.assertEquals(len(revision1.getFolderContents({'object_provides':IRevisionFile.__identifier__})), len(revision1_info.revisionfiles()))

    def test_revisionfiles_info1(self):
        """ All the revision files info, ordered """
        portal = self.layer['portal']
        revision1_info = self._revision1_info()
        self.assertEquals(revision1_info.revisionfiles_info()[0]['url'], '%s/view' % portal['revision1']['2'].absolute_url())
        self.assertEquals(revision1_info.revisionfiles_info()[1]['url'], '%s/view' % portal['revision1']['1'].absolute_url())
        self.assertEquals(revision1_info.revisionfiles_info()[2]['url'], '%s/view' % portal['revision1']['3'].absolute_url())

    def test_revisionfiles_info4(self):
        """ All the revision files info, ordered """
        portal = self.layer['portal']
        revision1 = self._revision1()
        revision1_info = self._revision1_info()
        self.assertEquals(revision1_info.revisionfiles_info()[0]['url'], '%s/view' % portal['revision1']['2'].absolute_url())
        self.assertEquals(revision1_info.revisionfiles_info()[1]['url'], '%s/view' % portal['revision1']['1'].absolute_url())
        self.assertEquals(revision1_info.revisionfiles_info()[2]['url'], '%s/view' % portal['revision1']['3'].absolute_url())

        # latest revision deleted
        revision1.manage_delObjects(['2'])

        self.assertEquals(revision1_info.revisionfiles_info()[0]['url'], '%s/view' % portal['revision1']['1'].absolute_url())
        self.assertEquals(revision1_info.revisionfiles_info()[1]['url'], '%s/view' % portal['revision1']['3'].absolute_url())

    def test_revision_folder(self):
        """ Returns the revision folder """
        revision1 = self._revision1()
        revision1_info = self._revision1_info()
        self.assertEquals(revision1, revision1_info.revision_folder())

    def test_next_code1(self):
        """ Returns the next revision code """
        revision1_info = self._revision1_info()
        self.assertEquals('4', revision1_info.next_code())

    def test_next_code2(self):
        """ Returns the next revision code """
        revision1_info = self._revision1_info()
        self.assertEquals('4', revision1_info.next_code())

        # let's create a new revision
        revision1 = self._revision1()
        revision1.invokeFactory('File', '4')
        revision14 = revision1['4']

        from zope.interface import alsoProvides
        from redomino.revision.interfaces import IRevisionFile
        alsoProvides(revision14, IRevisionFile)
        revision14.reindexObject()

        self.assertEquals('5', revision1_info.next_code())

        # ok, now let's delete the revision '1'
        revision1.manage_delObjects(['4'])

        self.assertEquals('4', revision1_info.next_code())


class TestRevisionFilePolicy1(TestRevisionFileMixin, unittest.TestCase):
    layer = REDOMINO_REVISION_INTEGRATION_TESTING1

    def test_latest_priority_map1(self):
        """ The latest revision """

        portal = self.layer['portal']
        revision1_info = self._revision1_info()
        self.assertEquals(revision1_info.latest(), portal['revision1']['1'])


class TestRevisionFilePolicy2(TestRevisionFileMixin, unittest.TestCase):
    layer = REDOMINO_REVISION_INTEGRATION_TESTING2

    def test_latest_priority_map2(self):
        """ The latest revision """

        portal = self.layer['portal']
        revision1_info = self._revision1_info()
        self.assertEquals(revision1_info.latest(), portal['revision1']['2'])


class TestRevisionFilePolicy3(TestRevisionFileMixin, unittest.TestCase):
    layer = REDOMINO_REVISION_INTEGRATION_TESTING3

    def test_revisionfiles_info2(self):
        """ All the revision files info, ordered """

        portal = self.layer['portal']
        revision1_info = self._revision1_info()
        self.assertEquals(revision1_info.revisionfiles_info()[0]['url'], '%s/view' % portal['revision1']['1'].absolute_url())
        self.assertEquals(revision1_info.revisionfiles_info()[1]['url'], '%s/view' % portal['revision1']['3'].absolute_url())
        self.assertEquals(revision1_info.revisionfiles_info()[2]['url'], '%s/view' % portal['revision1']['2'].absolute_url())

        setRoles(portal, TEST_USER_ID, ['Manager'])
        portal['revision1']['3'].content_status_modify('publish')
        setRoles(portal, TEST_USER_ID, ['Member'])
        portal['revision1']['3'].reindexObject()

        self.assertEquals(revision1_info.revisionfiles_info()[0]['url'], '%s/view' % portal['revision1']['1'].absolute_url()) # published, 2012/04/06
        self.assertEquals(revision1_info.revisionfiles_info()[1]['url'], '%s/view' % portal['revision1']['3'].absolute_url()) # published, 2012/03/07
        self.assertEquals(revision1_info.revisionfiles_info()[2]['url'], '%s/view' % portal['revision1']['2'].absolute_url()) # private

    def test_revisionfiles_info3(self):
        """ All the revision files info, ordered """
        portal = self.layer['portal']
        revision1_info = self._revision1_info()
        self.assertEquals(revision1_info.revisionfiles_info()[0]['url'], '%s/view' % portal['revision1']['1'].absolute_url())
        self.assertEquals(revision1_info.revisionfiles_info()[1]['url'], '%s/view' % portal['revision1']['3'].absolute_url())
        self.assertEquals(revision1_info.revisionfiles_info()[2]['url'], '%s/view' % portal['revision1']['2'].absolute_url())

        portal['revision1']['1'].setEffectiveDate(None)
        portal['revision1']['2'].setEffectiveDate(None)
        portal['revision1']['3'].setEffectiveDate(None)
        portal['revision1']['1'].reindexObject()
        portal['revision1']['2'].reindexObject()
        portal['revision1']['3'].reindexObject()

        setRoles(portal, TEST_USER_ID, ['Manager'])
        portal['revision1']['3'].content_status_modify('publish')
        setRoles(portal, TEST_USER_ID, ['Member'])
        portal['revision1']['3'].reindexObject()

        self.assertEquals(revision1_info.revisionfiles_info()[0]['url'], '%s/view' % portal['revision1']['3'].absolute_url()) # newest published
        self.assertEquals(revision1_info.revisionfiles_info()[1]['url'], '%s/view' % portal['revision1']['1'].absolute_url()) # published
        self.assertEquals(revision1_info.revisionfiles_info()[2]['url'], '%s/view' % portal['revision1']['2'].absolute_url()) # private


class TestRevisionDocumentMixin():

    def _revision2(self):
        portal = self.layer['portal']

        return portal['revision2']

    def _revision2_info(self):
        from redomino.revision.interfaces import IRevisionInfo
        portal = self.layer['portal']

        revision2 = portal['revision2']
        return IRevisionInfo(revision2)

    def _revision3(self):
        portal = self.layer['portal']

        return portal['revision3']

    def _revision3_info(self):
        from redomino.revision.interfaces import IRevisionInfo
        portal = self.layer['portal']

        revision3 = portal['revision3']
        return IRevisionInfo(revision3)


class TestRevisionDocument(TestRevisionDocumentMixin, unittest.TestCase):
    layer = REDOMINO_REVISION_INTEGRATION_TESTING
    
    def test_latest(self):
        """ The latest revision """
        portal = self.layer['portal']
        revision2_info = self._revision2_info()
        self.assertEquals(revision2_info.latest(), portal['revision2']['2'])

    def test_revision_without_effective_date(self):
        """ The latest revision """
        portal = self.layer['portal']
        revision3 = self._revision3()
        revision3_info = self._revision3_info()

        # this is the only one and latest revision
        self.assertEquals(revision3_info.latest(), portal['revision3']['1'])
        self.assertFalse('2' in revision3.objectIds())

        from zope.component import getMultiAdapter
        view = getMultiAdapter((revision3['1'], revision3['1'].REQUEST), name='clone_revision')

        # cloned revision1
        view()

        # revision1 should be the latest because both 1 and 2 doesn't have an effective date, so the latest should be the previous one 
        self.assertEquals(revision3_info.latest(), portal['revision3']['1'])
        self.assertTrue('2' in revision3.objectIds())

        # now we set the effective date to revision 2
        from DateTime import DateTime
        revision3['2'].setEffectiveDate(DateTime())
        revision3['2'].reindexObject()

        self.assertEquals(revision3_info.latest(), portal['revision3']['2'])

    def test_revision_without_effective_date2(self):
        """ The latest revision. It works for > 10 revisions? """
        portal = self.layer['portal']
        revision3 = self._revision3()
        revision3_info = self._revision3_info()

        # this is the only one and latest revision
        self.assertEquals(revision3_info.latest(), portal['revision3']['1'])
        self.assertFalse('2' in revision3.objectIds())

        from zope.component import getMultiAdapter
        view = getMultiAdapter((revision3['1'], revision3['1'].REQUEST), name='clone_revision')

        # cloned revision1
        view()
        view()
        view()
        view()
        view()
        view()
        view()
        view()
        view()
        view()

        # revision1 should be the latest because both 1 and 2 doesn't have an effective date, so the latest should be the previous one 
        self.assertEquals(revision3_info.latest(), portal['revision3']['1'])
        self.assertTrue('11' in revision3.objectIds())


class TestRevisionDocumentPolicy4(TestRevisionDocumentMixin, unittest.TestCase):
    layer = REDOMINO_REVISION_INTEGRATION_TESTING4
    
    def test_latest_priority_map1(self):
        """ The latest revision """

        portal = self.layer['portal']
        revision2_info = self._revision2_info()
        self.assertEquals(revision2_info.latest(), portal['revision2']['1'])

    def test_revisionfiles_info2(self):
        """ All the revision files info, ordered """
        portal = self.layer['portal']
        revision2_info = self._revision2_info()
        self.assertEquals(revision2_info.revisionfiles_info()[0]['url'], portal['revision2']['1'].absolute_url())
        self.assertEquals(revision2_info.revisionfiles_info()[1]['url'], portal['revision2']['3'].absolute_url())
        self.assertEquals(revision2_info.revisionfiles_info()[2]['url'], portal['revision2']['2'].absolute_url())

        setRoles(portal, TEST_USER_ID, ['Manager'])
        portal['revision2']['3'].content_status_modify('publish_internally')
        setRoles(portal, TEST_USER_ID, ['Member'])
        portal['revision2']['3'].reindexObject()

        self.assertEquals(revision2_info.revisionfiles_info()[0]['url'], portal['revision2']['1'].absolute_url()) # internally published, date 2012/04/06
        self.assertEquals(revision2_info.revisionfiles_info()[1]['url'], portal['revision2']['3'].absolute_url()) # internally published, date 2012/03/07
        self.assertEquals(revision2_info.revisionfiles_info()[2]['url'], portal['revision2']['2'].absolute_url()) # internal

        # and now let's send the revision23 to the obsolete status
        setRoles(portal, TEST_USER_ID, ['Manager'])
        portal['revision2']['3'].content_status_modify('publish_externally')
        setRoles(portal, TEST_USER_ID, ['Member'])
        portal['revision2']['3'].reindexObject()

        self.assertEquals(revision2_info.revisionfiles_info()[0]['url'], portal['revision2']['1'].absolute_url())
        self.assertEquals(revision2_info.revisionfiles_info()[1]['url'], portal['revision2']['2'].absolute_url())
        self.assertEquals(revision2_info.revisionfiles_info()[2]['url'], portal['revision2']['3'].absolute_url())  # archived

    def test_revisionfiles_info3(self):
        """ All the revision files info, ordered """
        portal = self.layer['portal']

        portal['revision2']['1'].setEffectiveDate(None)
        portal['revision2']['2'].setEffectiveDate(None)
        portal['revision2']['3'].setEffectiveDate(None)
        portal['revision2']['1'].reindexObject()
        portal['revision2']['2'].reindexObject()
        portal['revision2']['3'].reindexObject()

        revision2_info = self._revision2_info()
        self.assertEquals(revision2_info.revisionfiles_info()[0]['url'], portal['revision2']['1'].absolute_url())
        self.assertEquals(revision2_info.revisionfiles_info()[1]['url'], portal['revision2']['3'].absolute_url())
        self.assertEquals(revision2_info.revisionfiles_info()[2]['url'], portal['revision2']['2'].absolute_url())

        setRoles(portal, TEST_USER_ID, ['Manager'])
        portal['revision2']['3'].content_status_modify('publish_internally')
        setRoles(portal, TEST_USER_ID, ['Member'])
        portal['revision2']['3'].reindexObject()

        self.assertEquals(revision2_info.revisionfiles_info()[0]['url'], portal['revision2']['3'].absolute_url()) # internally published (newest pub date)
        self.assertEquals(revision2_info.revisionfiles_info()[1]['url'], portal['revision2']['1'].absolute_url()) # internally published
        self.assertEquals(revision2_info.revisionfiles_info()[2]['url'], portal['revision2']['2'].absolute_url()) # internal

        # and now let's send the revision23 to the obsolete status
        setRoles(portal, TEST_USER_ID, ['Manager'])
        portal['revision2']['3'].content_status_modify('publish_externally')
        setRoles(portal, TEST_USER_ID, ['Member'])
        portal['revision2']['3'].reindexObject()

        self.assertEquals(revision2_info.revisionfiles_info()[0]['url'], portal['revision2']['1'].absolute_url())
        self.assertEquals(revision2_info.revisionfiles_info()[1]['url'], portal['revision2']['2'].absolute_url())
        self.assertEquals(revision2_info.revisionfiles_info()[2]['url'], portal['revision2']['3'].absolute_url())  # archived

    def test_revision_without_effective_date_priority_map(self):
        """ The latest revision. It works for > 10 revisions and priority map? """

        portal = self.layer['portal']
        revision3 = self._revision3()
        revision3_info = self._revision3_info()

        # this is the only one and latest revision
        self.assertEquals(revision3_info.latest(), portal['revision3']['1'])
        self.assertFalse('2' in revision3.objectIds())

        from zope.component import getMultiAdapter
        view = getMultiAdapter((revision3['1'], revision3['1'].REQUEST), name='clone_revision')

        # cloned revision1
        for count in range(1, 20):
            view()

        # revision20 (the latest published item) 
        self.assertEquals(revision3_info.latest(), portal['revision3']['20'])

    def test_revision_without_effective_date_priority_map2(self):
        """ The latest revision. It works for > 10 revisions and priority map? """

        portal = self.layer['portal']
        revision3 = self._revision3()
        revision3_info = self._revision3_info()

        # this is the only one and latest revision
        self.assertEquals(revision3_info.latest(), portal['revision3']['1'])
        self.assertFalse('2' in revision3.objectIds())

        from zope.component import getMultiAdapter
        view = getMultiAdapter((revision3['1'], revision3['1'].REQUEST), name='clone_revision')

        # cloned revision1
        for count in range(1, 20):
            view()

        # revision1 should be the latest because both 1 and 2 doesn't have an effective date, so the latest should be the previous one 
        self.assertEquals(revision3_info.latest(), portal['revision3']['20'])

        revision3['11'].content_status_modify('submit')
        revision3['11'].reindexObject()

        # revision11 should be the latest (because pending > internal and the 20-th element is the previous one) 
        self.assertEquals(revision3_info.latest(), portal['revision3']['11'])
        self.assertEquals(revision3_info.revisionfiles()[1], portal['revision3']['20'])

        from DateTime import DateTime
        revision3['5'].setEffectiveDate(DateTime())
        revision3['5'].reindexObject()

        # revision11 should be the latest (because pending > internal, then 5 and 20) 
        self.assertEquals(revision3_info.latest(), portal['revision3']['11'])
        self.assertEquals(revision3_info.revisionfiles()[1], portal['revision3']['5'])
        self.assertEquals(revision3_info.revisionfiles()[2], portal['revision3']['20'])

