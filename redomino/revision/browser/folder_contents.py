from zope.component import getMultiAdapter
from Products.Five.browser import BrowserView


class FolderContentsView(BrowserView):
    """ Redirect on the parent folder contents (the revision and revision files are
        non structural items)
    """

    def __call__(self):
        revision_folder = self.context
        parent = getMultiAdapter((revision_folder, self.request), name=u"plone_context_state").parent()
        url = "%s/@@folder_contents" % parent.absolute_url()
        self.request.response.redirect(url)

