from zope.interface import implements
from plone.app.layout.globals.interfaces import IViewView

from Products.Five.browser import BrowserView

from redomino.revision.interfaces import IRevisionFileInfo
from redomino.revision.interfaces import IRevisionInfo
from redomino.revision.content.revisionfile import RevisionFileInfo
from redomino.revision.content.revision import RevisionInfo


class RevisionFileView(BrowserView, RevisionFileInfo):
    implements(IRevisionFileInfo, IViewView)

class RevisionView(BrowserView, RevisionInfo):
    """ Redirect on the """
    implements(IRevisionInfo, IViewView)

    def __call__(self):
        latest = self.latest()
        url = IRevisionFileInfo(latest).url()
        self.request.response.redirect(url)

