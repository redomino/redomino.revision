from operator import attrgetter

from Acquisition import aq_inner
from zope.interface import implements
from zope.component import adapts
from zope.component import queryUtility
from zope.component import getMultiAdapter

from redomino.revision.interfaces import IRevision
from redomino.revision.interfaces import IRevisionFile
from redomino.revision.interfaces import IRevisionInfo
from redomino.revision.interfaces import IRevisionFileInfo
from redomino.revision.interfaces import IRevisionWorkflowUtility


class RevisionInfo(object):
    """ The revision info adapter """
    implements(IRevisionInfo)
    adapts(IRevision)

    def __init__(self, context):
        self.context = context

    def _dictfy(self, item):
        revisionfile_info = IRevisionFileInfo(item)
        return dict(url=revisionfile_info.url(),
                    download_url=revisionfile_info.download_url(),
                    title=revisionfile_info.title(),
                    code=revisionfile_info.code(),
                    obj=item,
                    obj_info=revisionfile_info,
                   )

    def code(self):
        """ The revision code """
        return self.context.getId()

    def title(self):
        """ The revision title """
        return self.context.Title()

    def description(self):
        """ The revision description """
        return self.context.Description()

    def latest(self):
        """ The latest revision """
        revisionfiles = self.revisionfiles()
        return revisionfiles and revisionfiles[0]

    def latest_info(self):
        """ The latest revision info """
        latest = self.latest()
        return self._dictfy(latest)

    def revisionfiles(self, unrestricted=False):
        """ All the revision files, ordered """
        if unrestricted:
            catalog = getMultiAdapter((self.context, self.context.REQUEST), name=u'plone_tools').catalog()
            items = catalog.unrestrictedSearchResults(**{'object_provides':IRevisionFile.__identifier__,
                                                         'sort_order':'getId',
                                                         'path':'/'.join(self.context.getPhysicalPath())})
        else:
            items = self.context.getFolderContents({'object_provides':IRevisionFile.__identifier__,
                                                    'sort_order':'getId',
                                                   })
        items = sorted(items, key=attrgetter('effective'), reverse=True)
        if items:
            portal_type = items[0].portal_type
            priority_utility = queryUtility(IRevisionWorkflowUtility, name=portal_type)
            priority_utility = not priority_utility and queryUtility(IRevisionWorkflowUtility)

            if priority_utility:
                priority_map = priority_utility.priority_map()
                try:
                    items = sorted(items, key=lambda x: (priority_map.get(x.review_state, {}).get('priority'), x.effective))
                except TypeError:
                    # Missing.value on items[0].review_state
                    pass
                items.reverse()
        if unrestricted:
            return [item._unrestrictedGetObject() for item in items]
        else:
            return [item.getObject() for item in items]

                    
    def revisionfiles_info(self, unrestricted=False):
        """ All the revision files info, ordered """
        revisionfiles = self.revisionfiles(unrestricted)
        return [self._dictfy(item) for item in revisionfiles]

    def revision_folder(self):
        """ Returns the revision folder """
        return aq_inner(self.context)

    def next_code(self):
        """ Returns the next revision code """

        ids = [item.get('code') for item in self.revisionfiles_info(unrestricted=True)]
        max = 0
        for item in ids:
            item_int = 0
            try:
                item_int = int(item)
            except ValueError:
                pass
            if item_int > max:
                max = item_int
        return str(max + 1)

