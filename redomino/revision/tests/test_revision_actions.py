# coding=utf-8
import unittest2 as unittest

from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles

from Products.CMFCore.utils import getToolByName

from redomino.revision.testing import REDOMINO_REVISION_INTEGRATION_TESTING
from redomino.revision.testing import REDOMINO_REVISION_INTEGRATION_TESTING5


class TestCloneRevisionAction(unittest.TestCase):
    layer = REDOMINO_REVISION_INTEGRATION_TESTING

    def _revision1(self):
        portal = self.layer['portal']

        return portal['revision1']

    def _revision1_info(self):
        from redomino.revision.interfaces import IRevisionInfo
        portal = self.layer['portal']

        revision1 = portal['revision1']
        return IRevisionInfo(revision1)

    def test_clone_revision_view(self):
        """ The clone revision """
        revision1 = self._revision1()
        revision11 = revision1['1']

        from redomino.revision.browser.revision_actions import CloneRevisionView
        from zope.component import getMultiAdapter
        view = getMultiAdapter((revision11, revision11.REQUEST), name='clone_revision')
        self.assertIsInstance(view, CloneRevisionView)
        from redomino.revision.browser.interfaces import ICloneRevisionView
        self.assertTrue(ICloneRevisionView.implementedBy(CloneRevisionView))

    def test_clone_revision(self):
        """ The clone revision """
        revision1 = self._revision1()
        revision1_info = self._revision1_info()
        revision11 = revision1['1']

        self.assertEquals('4', revision1_info.next_code())
        self.assertFalse('4' in revision1.objectIds())

        latest = revision1_info.latest()

        from zope.component import getMultiAdapter
        view = getMultiAdapter((revision11, revision11.REQUEST), name='clone_revision')
        view()

        self.assertEquals('5', revision1_info.next_code())
        self.assertTrue('4' in revision1.objectIds())

        # ok, we have a cloned revision, let's see if all it's ok
        cloned_revision = revision1['4']
        from redomino.revision.interfaces import IRevisionFile
        IRevisionFile.providedBy(cloned_revision)

        # metadata ok?
        self.assertEquals(revision11.Title(), cloned_revision.Title())
        self.assertEquals(revision11.Description(), cloned_revision.Description())
        self.assertEquals(revision11.Subject(), cloned_revision.Subject())
        self.assertEquals(revision11.getRelatedItems(), cloned_revision.getRelatedItems())
        self.assertNotEquals(revision11.effective(), cloned_revision.effective())

        # latest ok?
        self.assertEquals(latest, revision1_info.latest())
        self.assertTrue(latest is not cloned_revision)


class TestEnableRevisionAction(unittest.TestCase):
    layer = REDOMINO_REVISION_INTEGRATION_TESTING

    def _revision1(self):
        portal = self.layer['portal']

        return portal['revision1']

    def _revision1_info(self):
        from redomino.revision.interfaces import IRevisionInfo
        portal = self.layer['portal']

        revision1 = portal['revision1']
        return IRevisionInfo(revision1)

    def test_enable_revision_view(self):
        """ The enable revision """
        revision1 = self._revision1()
        revision11 = revision1['1']

        from redomino.revision.browser.revision_actions import EnableRevisionView
        from zope.component import getMultiAdapter
        view = getMultiAdapter((revision11, revision11.REQUEST), name='enable_revision')
        self.assertIsInstance(view, EnableRevisionView)
        from redomino.revision.browser.interfaces import IEnableRevisionView
        self.assertTrue(IEnableRevisionView.implementedBy(EnableRevisionView))

    def test_enable_revision(self):
        """ """
        from DateTime import DateTime

        portal = self.layer['portal']

        setRoles(portal, TEST_USER_ID, ['Manager'])
        portal.invokeFactory('File', 'test.pdf')
        obj = portal['test.pdf']
        obj.setTitle('title')
        obj.setDescription('description')
        obj.setSubject(['keyword1'])
        obj.setRelatedItems([self._revision1()])
        obj.setEffectiveDate(DateTime())

        obj_title = obj.Title()
        obj_description = obj.Description()
        obj_subject = obj.Subject()
        obj_relateditems = obj.getRelatedItems()
        obj_effective = obj.effective()

        self.assertEquals('test.pdf', obj.getId())
        self.assertEquals('File', obj.portal_type)

        from zope.component import getMultiAdapter
        view = getMultiAdapter((obj, obj.REQUEST), name='enable_revision')
        view()

        obj = portal['test.pdf']

        self.assertEquals('test.pdf', obj.getId())
        self.assertEquals('Folder', obj.portal_type)
        self.assertTrue('1' in obj.objectIds())
        from redomino.revision.interfaces import IRevision
        self.assertTrue(IRevision.providedBy(obj))

        from redomino.revision.interfaces import IRevisionInfo
        revision_info = IRevisionInfo(obj)
        latest = revision_info.latest()

        # metadata ok?
        self.assertEquals(obj_title, latest.Title())
        self.assertEquals(obj_description, latest.Description())
        self.assertEquals(obj_subject, latest.Subject())
        self.assertEquals(obj_relateditems, latest.getRelatedItems())
        self.assertEquals(obj_effective, latest.effective())

        setRoles(portal, TEST_USER_ID, ['Member'])

class TestEnableRevisionSimpleAction(unittest.TestCase):
    """ Test enable revision with a workflow policy priority map on
        a standard Plone site (files without workflow) """
    layer = REDOMINO_REVISION_INTEGRATION_TESTING5

    def test_enable_revision(self):
        """ """

        portal = self.layer['portal']

        setRoles(portal, TEST_USER_ID, ['Manager'])
        portal.invokeFactory('File', 'test.pdf')
        obj = portal['test.pdf']
        obj.setTitle('title')
        obj.setDescription('description')
        obj.setSubject(['keyword1'])

        obj_title = obj.Title()
        obj_description = obj.Description()
        obj_subject = obj.Subject()

        self.assertEquals('test.pdf', obj.getId())
        self.assertEquals('File', obj.portal_type)

        from zope.component import getMultiAdapter
        view = getMultiAdapter((obj, obj.REQUEST), name='enable_revision')
        view()

        self.assertTrue(portal.hasObject('test.pdf'))

        obj = portal['test.pdf']

        self.assertEquals('test.pdf', obj.getId())
        self.assertEquals('Folder', obj.portal_type)
        self.assertTrue('1' in obj.objectIds())
        from redomino.revision.interfaces import IRevision
        self.assertTrue(IRevision.providedBy(obj))

        from redomino.revision.interfaces import IRevisionInfo
        revision_info = IRevisionInfo(obj)
        latest = revision_info.latest()

        # metadata ok?
        self.assertEquals(obj_title, latest.Title())
        self.assertEquals(obj_description, latest.Description())
        self.assertEquals(obj_subject, latest.Subject())

        revision1 = portal['test.pdf']
        revision1_info = IRevisionInfo(revision1)
        revision11 = revision1['1']
        portal_workflow = portal.portal_workflow
        self.assertEquals(portal_workflow.getInfoFor(revision1, 'review_state'), 'internal')

        self.assertFalse('2' in revision1.objectIds())
        # clone revision
        view = getMultiAdapter((revision11, revision11.REQUEST), name='clone_revision')
        view()

        self.assertEquals('3', revision1_info.next_code())
        self.assertTrue('2' in revision1.objectIds())

        ppw = getToolByName(revision1, 'portal_placeful_workflow')
        from redomino.revision.interfaces import IRevisionWorkflowUtility

        portal_type = revision11.portal_type
        from zope.component import queryUtility
        priority_utility = queryUtility(IRevisionWorkflowUtility, name=portal_type)
        priority_utility = not priority_utility and queryUtility(IRevisionWorkflowUtility)
        policy_id = priority_utility.policy_id()
        config = ppw.getWorkflowPolicyConfig(revision1)
        self.assertEquals(config.getPolicyIn().getId(), policy_id)
        self.assertEquals(config.getPolicyBelow().getId(), policy_id)

        revision12 = revision1['2']
        revision12.content_status_modify('submit')
        revision12.reindexObject()

        self.assertEquals(revision12, revision1_info.latest())

        self.assertEquals(portal_workflow.getInfoFor(revision1, 'review_state'), 'pending')

        # new revision11 become pending, new current revision
        revision11.content_status_modify('submit')
        self.assertEquals(revision11, revision1_info.latest())
        self.assertEquals(portal_workflow.getInfoFor(revision1, 'review_state'), 'pending')

        # revision12 become internally_published, new current revision
        revision12.content_status_modify('publish_internally')
        self.assertEquals(revision12, revision1_info.latest())
        self.assertEquals(portal_workflow.getInfoFor(revision1, 'review_state'), 'internally_published')

        setRoles(portal, TEST_USER_ID, ['Member'])

    def test_enable_revision2(self):
        """ """
        from DateTime import DateTime

        portal = self.layer['portal']

        setRoles(portal, TEST_USER_ID, ['Manager'])
        portal.invokeFactory('File', 'test.pdf')
        obj = portal['test.pdf']
        obj.setTitle('title')
        obj.setDescription('description')
        obj.setSubject(['keyword1'])
        obj.setEffectiveDate(DateTime())

        obj_title = obj.Title()
        obj_description = obj.Description()
        obj_subject = obj.Subject()
        obj_effective = obj.effective()

        self.assertEquals('test.pdf', obj.getId())
        self.assertEquals('File', obj.portal_type)

        from zope.component import getMultiAdapter
        view = getMultiAdapter((obj, obj.REQUEST), name='enable_revision')
        view()

        self.assertTrue(portal.hasObject('test.pdf'))

        obj = portal['test.pdf']

        self.assertEquals('test.pdf', obj.getId())
        self.assertEquals('Folder', obj.portal_type)
        self.assertTrue('1' in obj.objectIds())
        from redomino.revision.interfaces import IRevision
        self.assertTrue(IRevision.providedBy(obj))

        from redomino.revision.interfaces import IRevisionInfo
        revision_info = IRevisionInfo(obj)
        latest = revision_info.latest()

        # metadata ok?
        self.assertEquals(obj_title, latest.Title())
        self.assertEquals(obj_description, latest.Description())
        self.assertEquals(obj_subject, latest.Subject())
        self.assertEquals(obj_effective, latest.effective())

        revision1 = portal['test.pdf']
        revision1_info = IRevisionInfo(revision1)
        revision11 = revision1['1']
        portal_workflow = portal.portal_workflow
        self.assertEquals(portal_workflow.getInfoFor(revision1, 'review_state'), 'internal')

        revision11.content_status_modify('submit')
        revision11.content_status_modify('publish_internally')

        self.assertFalse('2' in revision1.objectIds())
        # clone revision
        view = getMultiAdapter((revision11, revision11.REQUEST), name='clone_revision')
        view()

        self.assertEquals('3', revision1_info.next_code())
        self.assertTrue('2' in revision1.objectIds())

        ppw = getToolByName(revision1, 'portal_placeful_workflow')
        from redomino.revision.interfaces import IRevisionWorkflowUtility

        portal_type = revision11.portal_type
        from zope.component import queryUtility
        priority_utility = queryUtility(IRevisionWorkflowUtility, name=portal_type)
        priority_utility = not priority_utility and queryUtility(IRevisionWorkflowUtility)
        policy_id = priority_utility.policy_id()
        config = ppw.getWorkflowPolicyConfig(revision1)
        self.assertEquals(config.getPolicyIn().getId(), policy_id)
        self.assertEquals(config.getPolicyBelow().getId(), policy_id)

        revision12 = revision1['2']
        revision12.content_status_modify('submit')
        revision12.reindexObject()

        self.assertEquals(revision11, revision1_info.latest())

        self.assertEquals(portal_workflow.getInfoFor(revision1, 'review_state'), 'internally_published')

        # new revision12 become pending, new current revision
        revision12.content_status_modify('publish_internally')
        revision1_info.latest()
        IRevisionInfo(revision1).latest()
        self.assertEquals(revision12, revision1_info.latest())
        self.assertEquals(portal_workflow.getInfoFor(revision1, 'review_state'), 'internally_published')

        setRoles(portal, TEST_USER_ID, ['Member'])
