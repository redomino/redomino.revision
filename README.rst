redomino.revision
=================

redomino.revision is an experimental package, so don't use it in production unless you know well what you are doing.

One of the missing killer feature of Plone in intranets and collaboration portals is an effective document versioning system.
You might want to create a file or document, let other people use it while you are working on the next version.
Once approved the next version, all people will see the new current version but you can get also the older ones: thery are still available

This is a very hard task and it is even more hard writing a generic plugin that solves this problem.
This projects aims to perform this hard work in a "simple" way: just with standard/existing content types, marker interfaces, events, catalog indexers and viewlets/custom views. You can create a file or a document and enabling versioning if you want. So no new content types are added and you should be safe with future migrations.

How it works? Basically the enable revision action will cut and paste your object into a newly created folder with the same id. Now you can clone an existing revision, change workflow status, etc.
Each revision will be still a Plone object with its workflow status and permissions and with an autoincremental id (so if you enable versioning on /lorem-ipsum.pdf you will get something like that /lorem-ipsum.pdf/1).

Here it is the ``redomino.revision`` manifesto:

* automatic current version detection based on workflow states priority policy (optional, you'll have to write some code) or publication date (default)

* you should be warned if you are visiting a not current revision

* it should work also for files and other type of non folderish documents

* the revision folder should be shown, indexed and behave like the current revision and share icon, review state, modification dates, sharing

* revision clonation with one click

* using a workflow policy, once a new revisionfile is published (new current), the previous published revision (previous current) should automatically go to the obsolete statu

* same download and view user experience for versioned files and standard files

* it should be possible to have always a working permalink to the latest version or reference an older one

* autoincrement of versioning ids

There could be two generic policies for versioning:

- **default**: simple, based on publication date. The revision with the more recent publication date wins

- **advanced**: workflow based versioning policy. You must supply a plugins that provides a map of weighted workflow status. The object with the "higher" status workflow wins. Wo you can build your own workflow based versioning policy. For example draft, pending, approved, archived. You can provide different workflow maps providing a ZCA component depending on the portal types. You should write your own policy

The default policy is based on a simple mechanism: wins the version with the more recent publication date. 
It requires you to edit manually publication dates and it could be quite annoying.

Since real and complex team collaborative systems are heavily based on workflows and each portal might have its workflow work chain (private -> pending -> published VS private -> pending 1 -> pending 2 - published -> archived and so on), redomino.revision let you define your your own workflow policy because it is built with extensibility in mind.
So if you have a collaborative editing based on workflows you can write your plugin and provide your specific workflow priority map, without having to fork the original core.


.. figure:: https://raw.github.com/redomino/redomino.revision/master/docs/screenshots/revision_example_integration.png
    :figwidth: image

    redomino.revision in action. As you can see you can extend redomino.revision with extra plugins in order to provide new features
    

Workflow based versioning policy
--------------------------------

You can provide a custom workflow based policy in order to detect the hierarchy of all versions.

The status configuration is stored on a dict that provides a status priority.

This dict defines a status ordering, from the higher status (for example: published) to lower status (for example: new) and 
a transition map that let you sail up or down the status level.
This status map should be returned by a utility with a structure similar to the following one::

    
    PRIORITY_MAP = dict(default=dict())  
    
    PRIORITY_MAP['default']['status1'] = {'up':'trans0',   # to obsolete status status0 (each status not listed in the PRIORITY_MAP is considered as obsolete)
                                          'down':'trans2', # to the previous status status2
                                          'priority':3,
                                         }
    PRIORITY_MAP['default']['status2'] = {'up':'trans1',   # to the next status status1
                                          'down':'trans3', # to the previous status status3
                                          'priority':2,
                                         }
    PRIORITY_MAP['default']['status3'] = {'up':'trans2',   # to the next status status2
                                          'down':'trans4', # to the previous status status3
                                          'priority':1,
                                         }
    PRIORITY_MAP['default']['status4'] = {'up':'trans3',   # to the next status status3
                                          'down':'',       # no down transition, this is the ininitial state
                                          'priority':0,
                                         }

The status configuration is empty by default: we will consider the creation date as order criteria.

For example workflow.py::

    from zope.interface import implements
    
    from redomino.revision.interfaces import IRevisionWorkflowUtility
    
    class RevisionWorkflowUtility():
        implements(IRevisionWorkflowUtility)
    
        def __init__(self, policy_id, prioritymap):
            self._policy_id = policy_id
            self._prioritymap = prioritymap
    
        def policy_id(self):
            return self._policy_id
    
        def priority_map(self):
            return self._prioritymap
    
        def __call__(self):
            return self
    
    DMS_POLICY = {}
    DMS_POLICY['internally_published'] = {'up':'archive', 'down':'reject', 'priority':2}
    DMS_POLICY['pending'] = {'up':'publish_internally', 'down':'reject', 'priority':1}
    DMS_POLICY['private'] = {'up':'submit', 'down':'', 'priority':0}
    dms_policy = RevisionWorkflowUtility('dmspolicy', DMS_POLICY)

And YOURPACKAGE/profiles/default/componentregistry.xml::

    <?xml version="1.0"?>
    <componentregistry>
        <utilities>
            <!-- The default revision workflow utility -->
            <utility 
                interface="redomino.revision.interfaces.IRevisionWorkflowUtility"
                factory="YOURPACKAGE.workflow.dms_policy"
                />
        </utilities>
    </componentregistry>


See more examples in tests.

TODO
----

* remove italian comments

* check i18n

* this plugin is not complete, needs more work

* never tested on Dexterity content types, probably it needs extra work

Authors
-------

* Davide Moro <davide.moro@redomino.com> (@davidemoro)
* Fabrizio Reale <fabrizio.reale@redomino.com> (@realefab)

