import doctest
import unittest2 as unittest

from redomino.revision.testing import REDOMINO_REVISION_INTEGRATION_TESTING

def test_suite():
    suite = unittest.TestSuite()

#    indexers = doctest.DocTestSuite('redomino.revision.indexers')
#    indexers.layer = REDOMINO_REVISION_INTEGRATION_TESTING

#    suite.addTests([
#              indexers,
#            ])
    return suite
