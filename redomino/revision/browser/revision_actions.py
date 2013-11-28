import transaction
from ZODB.POSException import ConflictError
from Acquisition import aq_base
from AccessControl import SecurityManagement
from AccessControl import SpecialUsers

from OFS.CopySupport import sanity_check
from OFS.event import ObjectWillBeMovedEvent
from OFS.event import ObjectClonedEvent
from OFS import subscribers

from zope.interface import implements
from zope.interface import alsoProvides
from zope.component import getMultiAdapter
from zope.component import queryUtility
from zope.event import notify
from zope.lifecycleevent import ObjectMovedEvent
from zope.lifecycleevent import ObjectCopiedEvent
from zope.container.contained import notifyContainerModified

from Products.Five.browser import BrowserView
from Products.statusmessages.interfaces import IStatusMessage
from Products.CMFCore.utils import getToolByName

from redomino.revision import revisionMessageFactory as _
from redomino.revision.interfaces import IRevision
from redomino.revision.interfaces import IRevisionFile
from redomino.revision.interfaces import IRevisionInfo
from redomino.revision.interfaces import IRevisionFileInfo
from redomino.revision.interfaces import IRevisionWorkflowUtility
from redomino.revision.browser.interfaces import IEnableRevisionView
from redomino.revision.browser.interfaces import ICloneRevisionView


def _move(parent, obj, target, old_id, new_id):
    try:
        obj._notifyOfCopyTo(target, op=1)
    except ConflictError:
        raise
    except Exception, e:
        raise e

    # Are we trying to move into the same container that we copied from?
    if not sanity_check(target, obj):
        return False

    notify(ObjectWillBeMovedEvent(obj, parent, old_id, target, new_id))

    obj.manage_changeOwnershipType(explicit=1)

    try:
        parent._delObject(old_id, suppress_events=True)
    except TypeError:
        # BBB: removed in Zope 2.11
        parent._delObject(old_id)

    obj = aq_base(obj)
    obj._setId(new_id)

    try:
        target._setObject(new_id, obj, set_owner=0, suppress_events=True)
    except TypeError:
        # BBB: removed in Zope 2.11
        target._setObject(new_id, obj, set_owner=0)
    obj = target._getOb(new_id)

    notify(ObjectMovedEvent(obj, parent, old_id, target, new_id))
    notifyContainerModified(parent)
    if aq_base(parent) is not aq_base(target):
        notifyContainerModified(target)

    obj._postCopy(target, op=1)

    # try to make ownership implicit if possible
    obj.manage_changeOwnershipType(explicit=0)

def _copy(parent, obj, target, old_id, new_id):
    try:
        obj._notifyOfCopyTo(target, op=0)
    except ConflictError:
        raise
    except Exception, e:
        raise e

    orig_obj = obj
    obj = obj._getCopy(target)
    obj._setId(new_id)

    notify(ObjectCopiedEvent(obj, orig_obj))

    target._setObject(new_id, obj)
    obj = target._getOb(new_id)
    obj.wl_clearLocks()

    obj._postCopy(target, op=0)

    subscribers.compatibilityCall('manage_afterClone', obj, obj)

    notify(ObjectClonedEvent(obj))

class EnableRevisionView(BrowserView):
    """ Clone revision view """
    implements(IEnableRevisionView)


    def __call__(self):
        """ Create a new revision folder based on an existing item """
        context_id = self.context.getId()
        parent = getMultiAdapter((self.context, self.request), name=u'plone_context_state').parent()
        try:
            uniqueid = parent.generateUniqueId('Folder')
            uniqueid = parent.invokeFactory('Folder', uniqueid)
            folderish_obj = getattr(parent, uniqueid)

            folderish_obj.setTitle(self.context.Title())

            alsoProvides(folderish_obj, IRevision)

            revision_info = IRevisionInfo(folderish_obj)
            next_code = revision_info.next_code()

            transaction.savepoint(optimistic=True)

            _move(parent, self.context, folderish_obj, context_id, next_code)

            revisionfile = getattr(folderish_obj, next_code)
            alsoProvides(revisionfile, IRevisionFile)

            _move(parent, folderish_obj, parent, uniqueid, context_id)

            newcontext = getattr(parent, context_id)
            ppw = getToolByName(newcontext, 'portal_placeful_workflow', None)
            if ppw:
                portal_type = self.context.portal_type
                priority_utility = queryUtility(IRevisionWorkflowUtility, name=portal_type)
                priority_utility = not priority_utility and queryUtility(IRevisionWorkflowUtility)
                policy_id = priority_utility and priority_utility.policy_id()
                if policy_id and ppw.isValidPolicyName(policy_id):

                    old_sm = SecurityManagement.getSecurityManager()
                    try:
                        SecurityManagement.newSecurityManager(None, SpecialUsers.system)
                        newcontext.manage_addProduct['CMFPlacefulWorkflow'].manage_addWorkflowPolicyConfig()
                        config = ppw.getWorkflowPolicyConfig(newcontext)
                        config.setPolicyIn(policy=policy_id)
                        config.setPolicyBelow(policy=policy_id, update_security=True)
                    finally:
                        SecurityManagement.setSecurityManager(old_sm)
            newcontext.reindexObject()
            newcontext.reindexObjectSecurity()
                
        except ConflictError:
            raise
        except Exception:
            view_url = getMultiAdapter((self.context, self.request), name=u'plone_context_state').view_url()
            self.request.response.redirect(view_url)
            IStatusMessage(self.request).addStatusMessage(_(u'enabled_revision_error', default=u'Error'), type='error')
        else:
            view_url = getMultiAdapter((folderish_obj, self.request), name=u'plone_context_state').view_url()
            self.request.response.redirect(view_url)
            IStatusMessage(self.request).addStatusMessage(_(u'enabled_revision_ok', default=u'Revision created correctly'), type='info')


class CloneRevisionView(BrowserView):
    """ Clone revision view """
    implements(ICloneRevisionView)

    def __call__(self):
        """ Create a new revision based on an existing item IRevisionFile """
        revisionfile_info = IRevisionFileInfo(self.context)
        revision_folder = revisionfile_info.revision_folder()
        revision_info = IRevisionInfo(revision_folder)
        next_code = revision_info.next_code()

        try:
            _copy(revision_folder, self.context, revision_folder, self.context.getId(), next_code)

            cloned_revision = getattr(revision_folder, next_code)
            member = getMultiAdapter((self.context, self.request), name=u'plone_portal_state').member()
            creator = member.getId()
            cloned_revision.setCreators([creator])
            plone_utils = getToolByName(self.context, 'plone_utils')
            plone_utils.changeOwnershipOf(cloned_revision, member.getId())
            cloned_revision.setRelatedItems(self.context.getRelatedItems())
            cloned_revision.setEffectiveDate(None)
            cloned_revision.reindexObject()
            cloned_revision.reindexObjectSecurity()
        except ConflictError:
            raise
        except Exception:
            IStatusMessage(self.request).addStatusMessage(_(u'cloned_revision_error', default=u'Error'), type='error')
        else:
            IStatusMessage(self.request).addStatusMessage(_(u'cloned_revision_ok', default=u'Revision cloned correctly'), type='info')

        self.request.response.redirect("/".join(revision_folder.getPhysicalPath()))



