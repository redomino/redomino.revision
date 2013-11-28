from plone.app.layout.viewlets import ViewletBase

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from redomino.revision.interfaces import IRevisionInfo
from redomino.revision.interfaces import IRevisionFileInfo


class RevisionMetadataViewlet(ViewletBase):
    index = ViewPageTemplateFile('templates/metadata_viewlet.pt')

    def update(self):
        super(RevisionMetadataViewlet, self).update()

        self.revisionfile_info = IRevisionFileInfo(self.context)

class RevisionNotLatestViewlet(ViewletBase):
    index = ViewPageTemplateFile('templates/notlatest_viewlet.pt')

    def update(self):
        super(RevisionNotLatestViewlet, self).update()

        self.revisionfile_info = IRevisionFileInfo(self.context)
        self.latest = self.revisionfile_info.is_latest()

class RevisionListViewlet(ViewletBase):
    index = ViewPageTemplateFile('templates/revisionlist_viewlet.pt')

    def update(self):
        super(RevisionListViewlet, self).update()

        self.revisionfile_info = IRevisionFileInfo(self.context)
        self.revision_info = IRevisionInfo(self.revisionfile_info.revision_folder())
        self.revisions = sorted(self.revision_info.revisionfiles_info(), key = lambda o: o['obj_info'].code(), reverse = True)

