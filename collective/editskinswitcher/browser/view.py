from zope.annotation.interfaces import IAnnotations
from zope.publisher.browser import BrowserView
from persistent.mapping import PersistentMapping

from Acquisition import aq_inner

from Products.CMFPlone.utils import getToolByName
from Products.CMFPlone import PloneMessageFactory as _


ANNOTATION_KEY = "collective.editskinswitcher"


class SelectSkin(BrowserView):

    def __call__(self):
        skin_name = self.request.form.get("skin_name", None)
        annotations = IAnnotations(aq_inner(self.context))
        ns = annotations.get(ANNOTATION_KEY, None)
        if ns is None:
            ns = annotations[ANNOTATION_KEY] = PersistentMapping()
        ns["default-skin"] = skin_name

        utils = getToolByName(self.context, "plone_utils")
        utils.addPortalMessage(_(u"Skin changed."))
        return self.request.RESPONSE.redirect(self.context.absolute_url())
