from plone.app.layout.viewlets.common import ViewletBase
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.interface import implements
from plone.memoize.instance import memoize

class PreviewViewlet(ViewletBase):
    """ IFrame view on to default skin to preserve some WYSIWYG feel to the edit interface to be used to replace main content in standard view skins """
    render = ViewPageTemplateFile("templates/preview_viewlet.pt")

    @memoize
    def objectURL(self):
        context = self.context
        return context.absolute_url() + '/view?mutate_skin=default'        
