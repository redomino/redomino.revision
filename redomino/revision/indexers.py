from plone.indexer import indexer

from redomino.revision.interfaces import IRevision
from redomino.revision.interfaces import IRevisionFile
from redomino.revision.interfaces import IRevisionInfo
from redomino.revision.interfaces import IRevisionFileInfo

def _latest(revision):
    revision_info = IRevisionInfo(revision)
    latest = revision_info.latest()
    return latest

def _latest_info(revision):
    latest = _latest(revision)
    latest_info = IRevisionFileInfo(latest)
    return latest_info

@indexer(IRevision)
def title(obj):
    """ """
    latest_info = _latest_info(obj)

    return latest_info.title()

@indexer(IRevision)
def description(obj):
    """ """
    latest_info = _latest_info(obj)

    return latest_info.description()

@indexer(IRevision)
def get_icon(obj):
    """ """
    latest_info = _latest_info(obj)

    return latest_info.get_icon()

@indexer(IRevision)
def modified(obj):
    """ """
    latest_info = _latest_info(obj)

    return latest_info.modification_date()

@indexer(IRevision)
def get_size(obj):
    """ """
    latest_info = _latest_info(obj)

    return latest_info.get_size()

@indexer(IRevision)
def effective(obj):
    """ """
    latest_info = _latest_info(obj)

    return latest_info.publication_date()

@indexer(IRevision)
def effective_date(obj):
    """ """
    latest = _latest(obj)

    return latest.EffectiveDate()

@indexer(IRevision)
def subject(obj):
    """ """
    latest_info = _latest_info(obj)

    return latest_info.keywords()

@indexer(IRevision)
def creator(obj):
    """ """
    latest_info = _latest_info(obj)

    return latest_info.creator()

@indexer(IRevision)
def revision_code(obj):
    """ """
    latest_info = _latest_info(obj)

    return latest_info.code()

@indexer(IRevisionFile)
def revision_code_file(obj):
    """ """
    revisionfile_info = IRevisionFileInfo(obj)

    return revisionfile_info.code()

@indexer(IRevision)
def list_creators(obj):
    """ """
    latest = _latest(obj)

    return latest.listCreators()

@indexer(IRevision)
def portal_type(obj):
    """ """
    latest = _latest(obj)

    return latest.portal_type

@indexer(IRevision)
def meta_type(obj):
    """ """
    latest = _latest(obj)

    return latest.meta_type

@indexer(IRevision)
def type(obj):
    """ """
    latest = _latest(obj)

    return latest.Type()
