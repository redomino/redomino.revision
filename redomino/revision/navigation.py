from zope.component import adapts
from zope.interface import implements

from plone.app.portlets.portlets.navigation import NavtreeStrategy

from plone.app.portlets.portlets.navigation import INavigationPortlet
from plone.app.layout.navigation.interfaces import INavtreeStrategy

from redomino.revision.interfaces import IRevision
from redomino.revision.interfaces import IRevisionFile

class RevisionStrategy(NavtreeStrategy):
    """Revision strategy tree: when you are viewing a revision (folder)
       it does not show any sub item (revisionfiles)
    """
    implements(INavtreeStrategy)
    adapts(IRevision, INavigationPortlet)

    def nodeFilter(self, node):
        return False

    def subtreeFilter(self, node):
        return False

    def showChildrenOf(self, object):
        """Given an object (usually the root of the site), determine whether
           children should be shown or not. Even if this returns True, if
           showAllParents is True, the path to the current item may be shown.
        """
        return False


class RevisionFileStrategy(RevisionStrategy):
    """Revision strategy tree: when you are viewing a revision (folder)
       it does not show any sub item (revisionfiles)
    """
    implements(INavtreeStrategy)
    adapts(IRevisionFile, INavigationPortlet)

