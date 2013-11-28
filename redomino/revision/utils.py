from DateTime import DateTime
from zope.interface import alsoProvides
from redomino.revision.interfaces import IRevision
from redomino.revision.interfaces import IRevisionFile

def setup_contents(portal):
    # File
    portal.invokeFactory('Folder', 'revision1')
    revision1 = portal['revision1']
    revision1.setTitle('title')
    revision1.setDescription('description')
    alsoProvides(revision1, IRevision)

    revision1.invokeFactory('File', '1')
    revision11 = revision1['1']
    revision11.setTitle('1')
    revision11.setDescription('1')
    revision11.setSubject(['keyword1'])
    revision11.setCreationDate(DateTime())
    revision11.setEffectiveDate(DateTime())
    alsoProvides(revision11, IRevisionFile)

    revision11.content_status_modify('publish')

    revision1.invokeFactory('File', '2')
    revision12 = revision1['2']
    revision12.setTitle('2')
    revision12.setDescription('2')
    revision12.setCreationDate(DateTime()+12)
    revision12.setEffectiveDate(DateTime()+15)
    alsoProvides(revision12, IRevisionFile)

    revision1.invokeFactory('File', '3')
    revision13 = revision1['3']
    revision13.setTitle('3')
    revision13.setDescription('3')
    revision13.setCreationDate(DateTime()-30)
    revision13.setEffectiveDate(DateTime()-30)
    alsoProvides(revision13, IRevisionFile)

    revision13.content_status_modify('submit')

    portal.invokeFactory('Document', 'alien')
    alien = portal['alien']
    revision11.setRelatedItems([revision12, alien])
    revision12.setRelatedItems([revision11, alien])

    revision11.reindexObject()
    revision12.reindexObject()
    revision13.reindexObject()
    revision1.reindexObject()

    # Document
    portal.invokeFactory('Folder', 'revision2')
    revision2 = portal['revision2']
    revision2.setTitle('title')
    revision2.setDescription('description')
    alsoProvides(revision2, IRevision)

    revision2.invokeFactory('Document', '1')
    revision21 = revision2['1']
    revision21.setTitle('1')
    revision21.setDescription('1')
    revision21.setCreationDate(DateTime())
    revision21.setEffectiveDate(DateTime())
    alsoProvides(revision21, IRevisionFile)

    revision21.content_status_modify('publish_internally')

    revision2.invokeFactory('Document', '2')
    revision22 = revision2['2']
    revision22.setTitle('2')
    revision22.setDescription('2')
    revision22.setCreationDate(DateTime()+12)
    revision22.setEffectiveDate(DateTime()+15)
    alsoProvides(revision22, IRevisionFile)

    revision2.invokeFactory('Document', '3')
    revision23 = revision2['3']
    revision23.setTitle('3')
    revision23.setDescription('3')
    revision23.setCreationDate(DateTime()-30)
    revision23.setEffectiveDate(DateTime()-30)
    alsoProvides(revision23, IRevisionFile)

    revision23.content_status_modify('submit')

    alien = portal['alien']
    revision21.setRelatedItems([revision22, alien])
    revision22.setRelatedItems([revision21, alien])

    revision21.reindexObject()
    revision22.reindexObject()
    revision23.reindexObject()
    revision2.reindexObject()

    # Document2 (without effective date)
    portal.invokeFactory('Folder', 'revision3')
    revision3 = portal['revision3']
    revision3.setTitle('title')
    revision3.setDescription('description')
    alsoProvides(revision3, IRevision)

    revision3.invokeFactory('Document', '1')
    revision31 = revision3['1']
    revision31.setTitle('1')
    revision31.setDescription('1')
    revision31.setCreationDate(DateTime())
    alsoProvides(revision31, IRevisionFile)

    revision31.reindexObject()
    revision3.reindexObject()
