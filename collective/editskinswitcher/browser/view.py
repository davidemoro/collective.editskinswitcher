from persistent.mapping import PersistentMapping

from zope.annotation.interfaces import IAnnotations
from zope.publisher.browser import BrowserView

from Acquisition import aq_base, aq_inner
from ZPublisher.BeforeTraverse import registerBeforeTraverse

from Products.Five.component import LocalSiteHook, HOOK_NAME
from Products.SiteAccess.AccessRule import AccessRule

from Products.CMFPlone.utils import getToolByName
from Products.CMFPlone import PloneMessageFactory as _


ANNOTATION_KEY = "collective.editskinswitcher"


class SelectSkin(BrowserView):

    def __call__(self):
        # Check to see if the current object already has a
        # LocalSiteHook from Five registered. If not, then register
        # one ourselves, going around ``enableSite`` since we don't
        # want to make this object a full ``ISite``, but just get the
        # ``BeforeTraverseEvent`` fired.
        obj = aq_base(self.context)
        if not hasattr(obj, HOOK_NAME):
            hook = AccessRule(HOOK_NAME)
            registerBeforeTraverse(obj, hook, HOOK_NAME, 1)
            setattr(obj, HOOK_NAME, LocalSiteHook())

        annotations = IAnnotations(aq_inner(self.context))
        ns = annotations.get(ANNOTATION_KEY, None)
        if ns is None:
            ns = annotations[ANNOTATION_KEY] = PersistentMapping()

        skin_name = self.request.form.get("skin_name", None)
        ns["default-skin"] = skin_name

        utils = getToolByName(self.context, "plone_utils")
        utils.addPortalMessage(_(u"Skin changed."))
        return self.request.RESPONSE.redirect(self.context.absolute_url())
