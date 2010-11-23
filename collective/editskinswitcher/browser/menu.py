from plone.memoize.instance import memoize

from zope.interface import implements
from zope.component import getMultiAdapter

try:
    # Try import that works in Zope 2.13 or higher first
    from zope.browsermenu.menu import BrowserMenu
    from zope.browsermenu.menu import BrowserSubMenuItem
except ImportError:
    # BBB for Zope 2.12 or lower
    from zope.app.publisher.browser.menu import BrowserMenu
    from zope.app.publisher.browser.menu import BrowserSubMenuItem

from Products.CMFCore.utils import getToolByName
from Products.CMFPlone import utils

from collective.editskinswitcher.browser.interfaces import (
    ISkinsSubMenuItem, ISkinsMenu)
from collective.editskinswitcher.permissions import SetDefaultSkin
from collective.editskinswitcher.skin import get_selected_default_skin

class SkinsSubMenuItem(BrowserSubMenuItem):

    implements(ISkinsSubMenuItem)
    submenuId = "collective-editskinswitcher-menu-skins"
    title = u"Skins"
    description = u"Change skin for the current content item"
    extra = {'id': 'collective-editskinswitcher-menu-skins'}

    order = 11

    def __init__(self, context, request):
        BrowserSubMenuItem.__init__(self, context, request)
        self.tools = getMultiAdapter((context, request), name='plone_tools')
        self.context_state = getMultiAdapter((context, request),
                                             name='plone_context_state')

    @property
    def action(self):
        folder = self.context
        if not self.context_state.is_structural_folder():
            folder = utils.parent(self.context)
        return folder.absolute_url() + '/select_skin'

    @memoize
    def available(self):
        return (self._manageSkinSettings() and
                self.context_state.is_structural_folder())

    @memoize
    def _manageSkinSettings(self):
        return self.tools.membership().checkPermission(
            SetDefaultSkin, self.context)

    def selected(self):
        return False


class SkinsMenu(BrowserMenu):
    implements(ISkinsMenu)

    def getMenuItems(self, context, request):
        """Return menu item entries in a TAL-friendly form."""
        results = []

        skins_tool = getToolByName(context, "portal_skins")
        url = context.absolute_url()
        current_skin = get_selected_default_skin(context)
        for skin in skins_tool.getSkinSelections():
            skin_id = utils.normalizeString(skin, context, "utf-8")
            selected = skin == current_skin
            cssClass = selected and "actionMenuSelected" or "actionMenu"
            results.append(
                {"title": skin,
                 "description": u"Use '%s' skin for this folder" % skin,
                 "action": "%s/@@switchDefaultSkin?skin_name=%s" % (url, skin),
                 "selected": selected,
                 "extra": {
                     "id": "collective.editskinswitcher-skin-%s" % skin_id,
                     "separator": False,
                     "class": cssClass},
                 "submenu": None,
                 "icon": None,
                 })
        return results
