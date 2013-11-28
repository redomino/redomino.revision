from zope.interface import Interface


class IRevisionWorkflowUtility(Interface):
    """ Revision workflow utility.
        If you want register your named RevisionWorkflowUtility adding a componentregistry.xml

            <?xml version="1.0"?>
            <componentregistry>
                <utilities>
                    <!-- The default revision workflow utility -->
                    <utility 
                        interface="redomino.revision.interfaces.IRevisionWorkflowUtility"
                        factory="YOURPACKAGE.RevisionWorkflowUtility"
                        />
                    <!-- One or more revision workflow utilities for each portal type -->
                    <utility 
                        interface="redomino.revision.interfaces.IRevisionWorkflowUtility"
                        factory="YOURPACKAGE.RevisionWorkflowFileUtility"
                        name="File"
                        />
                    ...
                </utilities>
            </componentregistry>
    """

    def policy_id():
        """ Return the workflow policy id. You should provide a workflow policy id that
            assign the same workflow to revisioned item and revision folder.
        """

    def priority_map():
        """ Return the workflow policy priority map for the given policy_id.

            For example:
                PRIORITY_MAP = dict()
                PRIORITY_MAP['status1'] = {'up':'trans0',   # to obsolete status status0 (each status not listed in the PRIORITY_MAP is considered as obsolete)
                                           'down':'trans2', # to the previous status status2
                                           'priority':3,
                                                     }
                PRIORITY_MAP['status2'] = {'up':'trans1',   # to the next status status1
                                           'down':'trans3', # to the previous status status3
                                           'priority':2,
                                          }
                PRIORITY_MAP['status3'] = {'up':'trans2',   # to the next status status2
                                           'down':'trans4', # to the previous status status3
                                           'priority':1,
                                          }
                PRIORITY_MAP['status4'] = {'up':'trans3',   # to the next status status3
                                           'down':'',       # no down transition, this is the ininitial state
                                           'priority':0,
                                          }
                return PRIORITY_MAP                  
        """

    def __call__():
        """ The utility factory. Returns self """

class IRevisionable(Interface):
    """ Revisionable items """

class IRevision(Interface):
    """ The revision marker interface """

class IRevisionFile(Interface):
    """ The revision file marker interface """

class IRevisionInfo(Interface):
    """ The revision info adapter """

    def code():
        """ The revision code """

    def title():
        """ The revision title """

    def description():
        """ The revision description """

    def latest():
        """ The latest revision """

    def latest_info():
        """ The latest revision info """

    def revisionfiles(unrestricted=False):
        """ All the revision files, ordered """

    def revisionfiles_info(unrestricted=False):
        """ All the revision files info, ordered """

    def revision_folder():
        """ Returns the revision folder """

    def next_code():
        """ Returns the next revision code """


class IRevisionFileInfo(Interface):
    """ The revision file info adapter """

    def code():
        """ The revision file code """

    def parent_code():
        """ The parent revision file code """

    def title():
        """ The revision file title """

    def description():
        """ The revision file description """

    def keywords():
        """ The revision keywords """

    def creation_date():
        """ Creation date """

    def publication_date():
        """ Publication date"""

    def modification_date():
        """ Modification date"""

    def referring():
        """ Other revision files (IRevisionFile) related by this document """

    def referring_info():
        """ Other revision files info (IRevisionFile) related by this document """

    def referred_by():
        """ Other revision files (IRevisionFile) that refer this document """

    def referred_by_info():
        """ Other revision files info (IRevisionFile) that refer this document """

    def url():
        """ The view url """

    def download_url():
        """ The download url, if applicable """

    def status():
        """ The revisionfile status """

    def revision_folder():
        """ Returns the revision folder """

    def is_latest():
        """ Is the latest revision? """

    def base_url():
        """ The base url (absolute_url) """

    def creator():
        """ The creator id """

    def author():
        """ The memberinfo's creator """

    def authorname():
        """ The author name """

    def get_icon():
        """ The item icon """

    def get_size():
        """ The size object """

