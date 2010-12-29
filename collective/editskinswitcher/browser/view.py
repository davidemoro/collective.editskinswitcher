import logging
from zope.interface import alsoProvides, noLongerProvides
from Acquisition import aq_base, aq_inner
from Products.CMFPlone.utils import getToolByName
from plone.app.layout.navigation.interfaces import INavigationRoot
from Products.Five.component import LocalSiteHook, HOOK_NAME
from Products.SiteAccess.AccessRule import AccessRule
from ZPublisher.BeforeTraverse import registerBeforeTraverse
from ZPublisher.BeforeTraverse import unregisterBeforeTraverse
from zope.component import getUtility
from zope.publisher.browser import BrowserView

try:
    # Try import that works in Zope 2.13 or higher first
    from zope.browsermenu.interfaces import IBrowserMenu
    IBrowserMenu  # pyflakes
except ImportError:
    # BBB for Zope 2.12 or lower
    from zope.app.publisher.interfaces.browser import IBrowserMenu

from collective.editskinswitcher import SwitcherMessageFactory as _
from collective.editskinswitcher.skin import get_selected_default_skin
from collective.editskinswitcher.skin import set_selected_default_skin
from collective.editskinswitcher import config

logger = logging.getLogger('collective.editskinswitcher')


class SelectSkin(BrowserView):

    def update(self):
        """Set selected skin as the default for the current folder."""
        context = aq_inner(self.context)
        base_object = aq_base(context)
        utils = getToolByName(context, "plone_utils")

        # Which skin is requested?
        skin_name = self.request.form.get("skin_name", None)
        if skin_name is not None:
            skins_tool = getToolByName(context, 'portal_skins')
            if skin_name not in skins_tool.getSkinSelections():
                skin_name = None

        # Which skin is currently used as default skin, if any?
        current_skin = get_selected_default_skin(context)

        # Determine what needs to be done, and create or remove a
        # local site hook when needed.
        if skin_name is None and current_skin is None:
            utils.addPortalMessage(_(u"Nothing changed."))
        elif skin_name == current_skin:
            utils.addPortalMessage(_(u"Nothing changed."))
        elif skin_name is None and current_skin is not None:
            # Need to remove the hook.
            utils.addPortalMessage(_(u"No default skin selected anymore."))
            if hasattr(base_object, HOOK_NAME):
                logger.info("Unregistering before traverse hook at %s",
                            context.absolute_url())
                unregisterBeforeTraverse(base_object, HOOK_NAME)
                # Now we should be able to remove the local site hook.
                # But this might not always be the best idea.  Others
                # might be using the local site hook as well.  Let's
                # at least make it configurable:
                if config.REMOVE_LOCAL_SITE_HOOK:
                    logger.info("Removing local site hook at %s",
                                context.absolute_url())
                    delattr(base_object, HOOK_NAME)
                else:
                    logger.info("Keeping local site hook at %s",
                                context.absolute_url())
        else:
            # The normal case: a change to the default skin.
            utils.addPortalMessage(_(u"Skin changed."))

            # Check to see if the current object already has a
            # LocalSiteHook from Five registered. If not, then register
            # one ourselves, going around ``enableSite`` since we don't
            # want to make this object a full ``ISite``, but just get the
            # ``BeforeTraverseEvent`` fired.
            if not hasattr(base_object, HOOK_NAME):
                logger.info("Adding local site hook with before traverse hook "
                            "at %s", context.absolute_url())
                hook = AccessRule(HOOK_NAME)
                registerBeforeTraverse(base_object, hook, HOOK_NAME, 1)
                setattr(base_object, HOOK_NAME, LocalSiteHook())

        # Finally set the default skin.  Note that this is safe to
        # call when skin_name is None as well, as this cleans up a
        # possible earlier setting.
        set_selected_default_skin(context, skin_name)

        return self.request.RESPONSE.redirect(context.absolute_url())

    def menuItems(self):
        """Return the menu items for the skin switcher."""
        menu = getUtility(
            IBrowserMenu, name="collective-editskinswitcher-menu-skins",
            context=self.context)
        return menu.getMenuItems(self.context, self.request)


class NavigationRoot(BrowserView):

    def set_navigation_root(self):
        context = aq_inner(self.context)
        if not INavigationRoot.providedBy(context):
            alsoProvides(context, INavigationRoot)
            logger.info("Activated navigation root at %s",
                        context.absolute_url())
            utils = getToolByName(context, "plone_utils")
            utils.addPortalMessage(_(u"Activated navigation root."))
        return self.request.RESPONSE.redirect(context.absolute_url())

    def unset_navigation_root(self):
        context = aq_inner(self.context)
        if INavigationRoot.providedBy(context):
            noLongerProvides(context, INavigationRoot)
            logger.info("Deactivated navigation root at %s",
                        context.absolute_url())
            utils = getToolByName(context, "plone_utils")
            utils.addPortalMessage(_(u"Deactivated navigation root."))
        return self.request.RESPONSE.redirect(context.absolute_url())
