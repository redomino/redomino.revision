from DateTime import DateTime
from zope.component import queryUtility

from redomino.revision.interfaces import IRevisionFileInfo
from redomino.revision.interfaces import IRevisionInfo
from redomino.revision.interfaces import IRevisionWorkflowUtility

def revisionfile_modified(obj, event):
    """ Reindex the revision folder item """

    revisionfile_info = IRevisionFileInfo(obj)
    revision_folder = revisionfile_info.revision_folder()
    revision_folder.reindexObject()

def revisionfile_deleted(obj, event):
    """ Reindex the revision folder item """

    if obj is not event.object:
        return
    revisionfile_info = IRevisionFileInfo(obj)
    revision_folder = revisionfile_info.revision_folder()

    revision_info = IRevisionInfo(revision_folder)
    for revisionfile in revision_info.revisionfiles():
        revisionfile.reindexObject()
    revision_folder.reindexObject()

def revisionfile_copied(obj, event):
    
    current = event.object
    original = event.original
    
    localroles = original.get_local_roles()

    for user,roles in localroles:
         current.manage_setLocalRoles(user, roles)


def revisionfile_workflow(obj, event):
    """ Workflow state changed """
    priority_utility = queryUtility(IRevisionWorkflowUtility, name=obj.portal_type)
    priority_utility = not priority_utility and queryUtility(IRevisionWorkflowUtility)
    priority_map = priority_utility and priority_utility.priority_map()

    if priority_map:
        revisionfile_info = IRevisionFileInfo(obj)
        revision = revisionfile_info.revision_folder()
        revision_info = IRevisionInfo(revision)
        latest = revision_info.latest()
        obj_status = revisionfile_info.status()
        latestfile_info = IRevisionFileInfo(latest)
        latest_status = latestfile_info.status()
    
        
        if priority_map.get(obj_status, {}).get('priority', -1) >= priority_map.get(latest_status, {}).get('priority', -1):
            # set status
            workflow = event.workflow
            workflow.setStatusOf(workflow.getId(), revision, {'action': event.action, 'review_state': obj_status, 'comments': '', 'actor': '', 'time': DateTime()})
            workflow.updateRoleMappingsFor(revision)
            revision.reindexObject()
            revision.reindexObjectSecurity()
    
