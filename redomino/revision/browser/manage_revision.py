from zope.interface import alsoProvides

from plone.app.layout.globals.interfaces import IViewView

from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class ManageRevisionView(BrowserView):

    template = ViewPageTemplateFile('templates/manage_revision.pt')

    def __init__(self, context, request):
        alsoProvides(self, IViewView)
        super(ManageRevisionView, self).__init__(context, request)

    __call__ = template

