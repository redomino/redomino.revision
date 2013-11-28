# coding=utf-8

from plone.app.testing import PloneSandboxLayer 
from plone.app.testing import applyProfile
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import IntegrationTesting
from plone.app.testing import FunctionalTesting
from zope.configuration import xmlconfig

from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import login
from plone.app.testing import setRoles

from plone.testing import z2

class RevisionPolicy(PloneSandboxLayer):
    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load ZCML
        import redomino.revision.tests
        #  hack for plone.browserlayer
        xmlconfig.file('testing.zcml',
                       redomino.revision.tests,
                       context=configurationContext
                      )
        import redomino.revision
        xmlconfig.file('configure.zcml',
                       redomino.revision,
                       context=configurationContext
                      )

REDOMINO_REVISION_FIXTURE_BASE = RevisionPolicy()

class RevisionPolicyContents(PloneSandboxLayer):
    defaultBases = (REDOMINO_REVISION_FIXTURE_BASE,)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'redomino.revision:default')

        # setup contents
        setRoles(portal, TEST_USER_ID, ['Manager'])
        login(portal, TEST_USER_NAME)
        self._setup_workflow(portal)
        self._setup_contents(portal)
        setRoles(portal, TEST_USER_ID, ['Member'])

    def _setup_workflow(self, portal):
        from Products.CMFCore.utils import getToolByName

        workflowTool = getToolByName(portal, 'portal_workflow')

        workflowTool.setChainForPortalTypes(('File',), 'simple_publication_workflow')
        workflowTool.setChainForPortalTypes(('Document',), 'intranet_workflow')

    def _setup_contents(self, portal):
        from redomino.revision.utils import setup_contents
        setup_contents(portal)

REDOMINO_REVISION_FIXTURE = RevisionPolicyContents()

class RevisionPolicy1(PloneSandboxLayer):
    defaultBases = (REDOMINO_REVISION_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        super(RevisionPolicy1, self).setUpZope(app, configurationContext)
        # Load ZCML
        import redomino.revision.tests
        xmlconfig.file('policy1.zcml',
                       redomino.revision.tests,
                       context=configurationContext
                      )

    def setUpPloneSite(self, portal):
        super(RevisionPolicy1, self).setUpPloneSite(portal)
        applyProfile(portal, 'redomino.revision.tests:policy1')

class RevisionPolicy2(PloneSandboxLayer):
    defaultBases = (REDOMINO_REVISION_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        super(RevisionPolicy2, self).setUpZope(app, configurationContext)
        # Load ZCML
        import redomino.revision.tests
        xmlconfig.file('policy2.zcml',
                       redomino.revision.tests,
                       context=configurationContext
                      )

    def setUpPloneSite(self, portal):
        super(RevisionPolicy2, self).setUpPloneSite(portal)
        applyProfile(portal, 'redomino.revision.tests:policy2')

class RevisionPolicy3(PloneSandboxLayer):
    defaultBases = (REDOMINO_REVISION_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        super(RevisionPolicy3, self).setUpZope(app, configurationContext)
        # Load ZCML
        import redomino.revision.tests
        xmlconfig.file('policy3.zcml',
                       redomino.revision.tests,
                       context=configurationContext
                      )


    def setUpPloneSite(self, portal):
        super(RevisionPolicy3, self).setUpPloneSite(portal)
        applyProfile(portal, 'redomino.revision.tests:policy3')

class RevisionPolicy4(PloneSandboxLayer):
    defaultBases = (REDOMINO_REVISION_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        super(RevisionPolicy4, self).setUpZope(app, configurationContext)
        # Load ZCML
        import redomino.revision.tests
        xmlconfig.file('policy4.zcml',
                       redomino.revision.tests,
                       context=configurationContext
                      )


    def setUpPloneSite(self, portal):
        super(RevisionPolicy4, self).setUpPloneSite(portal)
        applyProfile(portal, 'redomino.revision.tests:policy4')

class RevisionPolicy5(PloneSandboxLayer):
    """ Standard workflow configuration (no create new contents, no customize default workflow) """
    defaultBases = (REDOMINO_REVISION_FIXTURE_BASE,)

    def setUpZope(self, app, configurationContext):
        super(RevisionPolicy5, self).setUpZope(app, configurationContext)
        # Load ZCML
        z2.installProduct(app, 'Products.CMFPlacefulWorkflow')
        import Products.CMFPlacefulWorkflow
        xmlconfig.file('configure.zcml',
                       Products.CMFPlacefulWorkflow,
                       context=configurationContext
                      )
        import redomino.revision.tests
        xmlconfig.file('policy5.zcml',
                       redomino.revision.tests,
                       context=configurationContext
                      )


    def setUpPloneSite(self, portal):
        super(RevisionPolicy5, self).setUpPloneSite(portal)
        # same workflow policy as RevisionPolicy4
        applyProfile(portal, 'Products.CMFPlacefulWorkflow:CMFPlacefulWorkflow')
        applyProfile(portal, 'redomino.revision.tests:policy5')

REDOMINO_REVISION_FIXTURE1 = RevisionPolicy1()
REDOMINO_REVISION_FIXTURE2 = RevisionPolicy2()
REDOMINO_REVISION_FIXTURE3 = RevisionPolicy3()
REDOMINO_REVISION_FIXTURE4 = RevisionPolicy4()
REDOMINO_REVISION_FIXTURE5 = RevisionPolicy5()

REDOMINO_REVISION_INTEGRATION_TESTING = IntegrationTesting(
                  bases=(REDOMINO_REVISION_FIXTURE,), 
                  name="RedominoRevision:Integration")
REDOMINO_REVISION_INTEGRATION_TESTING1 = IntegrationTesting(
                  bases=(REDOMINO_REVISION_FIXTURE1,), 
                  name="RedominoRevision1:Integration")
REDOMINO_REVISION_INTEGRATION_TESTING2 = IntegrationTesting(
                  bases=(REDOMINO_REVISION_FIXTURE2,), 
                  name="RedominoRevision2:Integration")
REDOMINO_REVISION_INTEGRATION_TESTING3 = IntegrationTesting(
                  bases=(REDOMINO_REVISION_FIXTURE3,), 
                  name="RedominoRevision3:Integration")
REDOMINO_REVISION_INTEGRATION_TESTING4 = IntegrationTesting(
                  bases=(REDOMINO_REVISION_FIXTURE4,), 
                  name="RedominoRevision4:Integration")
REDOMINO_REVISION_INTEGRATION_TESTING5 = IntegrationTesting(
                  bases=(REDOMINO_REVISION_FIXTURE5,), 
                  name="RedominoRevision5:Integration")
REDOMINO_REVISION_FUNCTIONAL_TESTING = FunctionalTesting(
        bases=(REDOMINO_REVISION_FIXTURE,), name="RedominoRevision:Functional")


