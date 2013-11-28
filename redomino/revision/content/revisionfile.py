from Acquisition import aq_base
from Acquisition import aq_inner
from Acquisition import aq_parent

from zope.interface import implements
from zope.component import adapts
from zope.component import getMultiAdapter

from Products.Archetypes.ExtensibleMetadata import FLOOR_DATE
from Products.CMFCore.utils import getToolByName

from redomino.revision.interfaces import IRevisionFile
from redomino.revision.interfaces import IRevisionFileInfo
from redomino.revision.interfaces import IRevisionInfo

class RevisionFileInfo(object):
    """ The revision file info adapter """
    implements(IRevisionFileInfo)
    adapts(IRevisionFile)
    
    def __init__(self, context):
        self.context = context

    def _dictfy(self, item):
        revisionfile_info = IRevisionFileInfo(item)
        return dict(url=revisionfile_info.url(), 
                    download_url=revisionfile_info.download_url(),
                    title=revisionfile_info.title(),
                    code=revisionfile_info.code(),
                    parent_code=revisionfile_info.parent_code(),
                    obj=item,
                    obj_info=revisionfile_info,
                   )

    def code(self):
        """ The revision file code """
        return self.context.getId()

    def parent_code(self):
        """ The parent revision file code """
        revision = self.revision_folder()
        return IRevisionInfo(revision).code()

    def title(self):
        """ The revision file title """
        return self.context.Title()

    def description(self):
        """ The revision file description """
        return self.context.Description()

    def keywords(self):
        """ The revision keywords """
        return self.context.Subject()

    def creation_date(self):
        """ Creation date """
        date = self.context.created()
        return date is not FLOOR_DATE and date or None

    def publication_date(self):
        """ Publication date"""
        date = self.context.effective()
        return date is not FLOOR_DATE and date or None

    def modification_date(self):
        """ Modification date"""
        date = self.context.modified()
        return date is not FLOOR_DATE and date or None

    def referring(self):
        """ Other revision files (IRevisionFile) related by this document """
        referring = [item for item in self.context.getRelatedItems() if IRevisionFile.providedBy(item)]
        return referring

    def referring_info(self):
        """ Other revision files info (IRevisionFile) related by this document """
        results = []
        for item in self.referring():
            results.append(self._dictfy(item))
        return sorted(results, key=lambda x: x['title'])

    def referred_by(self):
        """ Other revision files (IRevisionFile) that refer this document """
        referrers = [item for item in self.context.getBRefs('relatesTo') if IRevisionFile.providedBy(item)]
        return referrers

    def referred_by_info(self):
        """ Other revision files info (IRevisionFile) that refer this document """
        results = []
        for item in self.referred_by():
            results.append(self._dictfy(item))
        return sorted(results, key=lambda x: x['title'])

    def url(self):
        """ The view url """
        return getMultiAdapter((self.context, self.context.REQUEST), name=u'plone_context_state').view_url()
                   
    def download_url(self):
        """ The download url, if applicable """
        portal_properties = getToolByName(self.context, 'portal_properties', None)
        if portal_properties is not None:
            site_properties = getattr(portal_properties, 'site_properties', None)
            portal_type = getattr(aq_base(self.context), 'portal_type', None)
            if site_properties is not None and portal_type is not None:
                use_view_action = site_properties.getProperty('typesUseViewActionInListings', ())
                if portal_type in use_view_action:
                    return aq_inner(self.context).absolute_url()
        return None

    def status(self):
        """ The revisionfile status """
        workflow = getMultiAdapter((self.context, self.context.REQUEST), name=u'plone_tools').workflow()
        return workflow.getInfoFor(self.context, 'review_state', None)

    def revision_folder(self):
        """ Returns the revision folder """
        return aq_parent(aq_inner(self.context))

    def is_latest(self):
        """ Is the latest revision? """
        revision_folder = self.revision_folder()
        revision_folder_info = IRevisionInfo(revision_folder)
        return aq_inner(self.context) == revision_folder_info.latest()

    def base_url(self):
        """ The base url (absolute_url) """
        return getMultiAdapter((self.context, self.context.REQUEST), name=u'plone_context_state').object_url()

    def creator(self):
        """ The creator id """
        return self.context.Creator()

    def author(self):
        """ The memberinfo's creator """
        membership = getToolByName(self.context, 'portal_membership')
        return membership.getMemberInfo(self.creator())

    def authorname(self):
        """ The author name """
        author = self.author()
        return author and author['fullname'] or self.creator()

    def get_icon(self):
        """ The item icon """
        plone_layout = getMultiAdapter((self.context, self.context.REQUEST), name=u"plone_layout")
        icon = plone_layout.getIcon(self.context)
        return icon and icon.url

    def get_size(self):
        """ The size object """
        return self.context.get_size()



