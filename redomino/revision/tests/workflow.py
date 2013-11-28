from zope.interface import implements

from redomino.revision.interfaces import IRevisionWorkflowUtility

class RevisionWorkflowUtility():
    implements(IRevisionWorkflowUtility)

    def __init__(self, policy_id, prioritymap):
        self._policy_id = policy_id
        self._prioritymap = prioritymap

    def policy_id(self):
        return self._policy_id

    def priority_map(self):
        return self._prioritymap

    def __call__(self):
        return self

# policytest1
TEST_PRIORITYMAP1 = {}
TEST_PRIORITYMAP1['published'] = {'up':'', 'down':'reject', 'priority':1}
TEST_PRIORITYMAP1['private'] = {'up':'publish', 'down':'', 'priority':0}
policy1 = RevisionWorkflowUtility('policy1', TEST_PRIORITYMAP1)

# policytest2
TEST_PRIORITYMAP2 = {}
TEST_PRIORITYMAP2['published'] = {'up':'', 'down':'reject', 'priority':0}
TEST_PRIORITYMAP2['private'] = {'up':'publish', 'down':'', 'priority':1}
policy2 = RevisionWorkflowUtility('policy2', TEST_PRIORITYMAP2)

# policytest3
TEST_PRIORITYMAP3 = {}
TEST_PRIORITYMAP3['published'] = {'up':'', 'down':'reject', 'priority':2}
TEST_PRIORITYMAP3['pending'] = {'up':'publish', 'down':'', 'priority':1}
TEST_PRIORITYMAP3['private'] = {'up':'publish', 'down':'', 'priority':0}
policy3 = RevisionWorkflowUtility('policy3', TEST_PRIORITYMAP3)

# policytest4
TEST_PRIORITYMAP4 = {}
TEST_PRIORITYMAP4['internally_published'] = {'up':'publish_externally', 'down':'reject', 'priority':2}
TEST_PRIORITYMAP4['pending'] = {'up':'publish_internally', 'down':'reject', 'priority':1}
TEST_PRIORITYMAP4['internal'] = {'up':'submit', 'down':'', 'priority':0}
policy4 = RevisionWorkflowUtility('policy4', TEST_PRIORITYMAP4)

# policytest5
TEST_PRIORITYMAP5 = {}
TEST_PRIORITYMAP5['internally_published'] = {'up':'publish_externally', 'down':'reject', 'priority':2}
TEST_PRIORITYMAP5['pending'] = {'up':'publish_internally', 'down':'reject', 'priority':1}
TEST_PRIORITYMAP5['internal'] = {'up':'submit', 'down':'', 'priority':0}
policy5 = RevisionWorkflowUtility('policy5', TEST_PRIORITYMAP5)
