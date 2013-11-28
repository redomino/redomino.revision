from zope.interface import implements

from Products.Five.browser import BrowserView

from plone.app.layout.navigation.interfaces import IDefaultPage

from redomino.revision.interfaces import IRevisionInfo


class DefaultPage(BrowserView):
    implements(IDefaultPage)

    def isDefaultPage(self, obj, context_=None):
        """ This is needed in order to not display the revision items
            in the navigation portlet
        """
        return True

    def getDefaultPage(self):
        """Returns the id of the default page for the adapted object.
        """
        return IRevisionInfo(self.context).latest().getId()


