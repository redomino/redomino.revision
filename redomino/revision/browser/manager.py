from plone.app.viewletmanager.manager import OrderedViewletManager as _OrderedViewletManager
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class OrderedViewletManager(_OrderedViewletManager):
    template = ViewPageTemplateFile('templates/manager.pt')
