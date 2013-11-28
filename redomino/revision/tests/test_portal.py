import unittest2 as unittest
from redomino.revision.testing import REDOMINO_REVISION_INTEGRATION_TESTING

class TestSetup(unittest.TestCase):
    layer = REDOMINO_REVISION_INTEGRATION_TESTING

    def test_catalog_schema(self):
        """ All catalog metadatas correctly defined?? """
        portal = self.layer['portal']
        catalog_schema = portal.portal_catalog.schema()
        self.assertTrue('revision_code' in catalog_schema)

#    def test_catalog_indexes(self):
#        """ All catalog indexes correctly defined?? """
#        portal = self.layer['portal']
#        catalog_indexes = portal.portal_catalog.indexes()
#        self.assertTrue('ddt_quality_alert' in catalog_indexes)

    def test_atct_tool(self):
        """ Test metadata indexes and metadatas """
        portal = self.layer['portal']
        portal_atct = portal.portal_atct

#        # check indexes
#        indexes = portal_atct.getIndexes(enabledOnly=1)
#        self.assertTrue('ddt_quality_alert' in indexes)

#        # check criterions
#        quality_alert_criteria = portal_atct.getIndex('ddt_quality_alert').criteria
#        self.assertTrue(len(quality_alert_criteria)==1 and 'ATBooleanCriterion' in quality_alert_criteria)

        # check metadatas
        topic_metadata = portal_atct.topic_metadata
        self.assertTrue('revision_code' in topic_metadata)

    def test_css(self):
        """ Css resources loaded? """
        portal = self.layer['portal']
        portal_css = portal.portal_css
        resource_ids = [item.getId() for item in portal_css.resources]

        self.assertTrue('++resource++redomino.revision.resources/revision.css' in resource_ids)

    def test_portal_actions(self):
        """ Portal actions loaded? """
        portal = self.layer['portal']
        portal_actions = portal.portal_actions
        self.assertTrue('enable_revision' in portal_actions.object_buttons.objectIds())
