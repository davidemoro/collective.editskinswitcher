from Products.PloneTestCase import PloneTestCase as ptc
ptc.setupPloneSite()

from zope.annotation.interfaces import IAnnotations
from zope.component import getUtility

from collective.editskinswitcher.browser.interfaces import ISkinsMenu
from collective.editskinswitcher.browser.view import ANNOTATION_KEY
from collective.editskinswitcher.tests.utils import (
    FakeTraversalEvent, TestRequest, new_default_skin)
from collective.editskinswitcher.traversal import switch_skin

from Acquisition import aq_base
from ZPublisher.BeforeTraverse import queryBeforeTraverse

from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import normalizeString
from Products.Five.component import LocalSiteHook, HOOK_NAME
from Products.SiteAccess.AccessRule import AccessRule

# BBB Zope 2.12
try:
    from zope.browsermenu.interfaces import IBrowserMenu
except ImportError:
    from zope.app.publisher.interfaces.browser import IBrowserMenu


class TestContentMenu(ptc.PloneTestCase):

    def afterSetUp(self):
        self.menu = getUtility(
            IBrowserMenu, name="plone_contentmenu", context=self.folder)
        self.request = self.app.REQUEST

    # Skins sub-menu
    def testSkinsSubMenuIncludedForFolder(self):
        items = self.menu.getMenuItems(self.folder, self.request)
        skinsMenuItem = [
            i for i in items if
            i["extra"]["id"] == "collective.editskinswitcher-menu-skins"][0]
        self.assertEqual(skinsMenuItem["action"],
                         self.folder.absolute_url() + "/folder_contents")
        self.failUnless(len(skinsMenuItem["submenu"]) > 0)

    def testSkinsSubMenuNotIncludedForDocument(self):
        self.folder.invokeFactory("Document", "doc")
        items = self.menu.getMenuItems(self.folder.doc, self.request)
        skinsMenuItem = [
            i for i in items if
            i["extra"]["id"] == "collective.editskinswitcher-menu-skins"]
        self.failIf(len(skinsMenuItem) > 0)


    def testSkinsSubMenuNotIncludedForOtherMember(self):
        # The skins menu is only available for someone that has the
        # 'Add portal content' permission in the folder.
        membership_tool = getToolByName(self.folder, 'portal_membership')
        membership_tool.addMember('anotherMember', 'secret', ['Member'], [])
        self.login('anotherMember')
        items = self.menu.getMenuItems(self.folder, self.request)
        skinsMenuItem = [
            i for i in items if
            i["extra"]["id"] == "collective.editskinswitcher-menu-skins"]
        self.failIf(len(skinsMenuItem) > 0)


class TestSkinsMenu(ptc.PloneTestCase):

    def afterSetUp(self):
        self.menu = getUtility(
            IBrowserMenu, name="collective.editskinswitcher-menu-skins",
            context=self.folder)
        self.request = self.app.REQUEST

    def testSkinsMenuImplementsIBrowserMenu(self):
        self.failUnless(IBrowserMenu.providedBy(self.menu))

    def testSkinsMenuImplementsISkinsMenu(self):
        self.failUnless(ISkinsMenu.providedBy(self.menu))

    def testSkinsMenuFindsSkins(self):
        st = getToolByName(self.folder, "portal_skins")
        skins = st.getSkinSelections()
        actions = self.menu.getMenuItems(self.folder, self.request)
        self.assertEqual(set(skins),
                         set([a["title"] for a in actions]))
        self.assertEqual(u"Use '%s' skin for this folder" % actions[0]["title"],
                         actions[0]["description"])
        param = "selectSkin?skin_name=%s" % actions[0]["title"]
        self.assertEqual(param, actions[0]["action"].split("@@")[1])
        skin_id = normalizeString(actions[0]["title"])
        self.assertEqual("collective.editskinswitcher-skin-%s" % skin_id,
                         actions[0]["extra"]["id"])


class TestSelectSkinView(ptc.FunctionalTestCase):

    def afterSetUp(self):
        self.basic_auth = "%s:%s" % (ptc.default_user, ptc.default_password)
        self.folder_path = self.folder.absolute_url(1)
        self.portal_path = self.portal.absolute_url(1)

    def testSwitchDefaultSkin(self):
        response = self.publish(
            self.folder_path + '/@@switchDefaultSkin?skin_name=Plone%20Default',
            basic=self.basic_auth)
        self.assertEqual(response.getStatus(), 302)
        self.assertEqual(self.folder.absolute_url(),
                         response.getHeader("Location"))
        self.assertTrue(hasattr(aq_base(self.folder), HOOK_NAME))
        self.assertTrue(isinstance(getattr(aq_base(self.folder), HOOK_NAME),
                                   LocalSiteHook))

        btr = queryBeforeTraverse(self.folder, HOOK_NAME)[0]
        self.assertEqual(1, btr[0])
        self.assertTrue(isinstance(btr[1], AccessRule))
        self.assertEqual(HOOK_NAME, btr[1].name)
        ns = IAnnotations(self.folder).get(ANNOTATION_KEY, None)
        self.assertNotEqual(None, ns)
        self.assertEqual("Plone Default", ns["default-skin"])

    def testAnotherMemberCannotSelectSkin(self):
        membership_tool = getToolByName(self.folder, 'portal_membership')
        membership_tool.addMember("anotherMember", "secret", ['Member'], [])
        response = self.publish(
            self.folder_path + '/@@switchDefaultSkin?skin_name=Plone%20Default',
            basic="anotherMember:secret")
        self.assertEqual(response.getStatus(), 302)
        self.assertFalse(self.folder.absolute_url() ==
                         response.getHeader("Location"))
        self.assertFalse(hasattr(aq_base(self.folder), HOOK_NAME))
        ns = IAnnotations(self.folder).get(ANNOTATION_KEY, None)
        self.assertEqual(None, ns)

    def testSkinSwitchedOnFakeTraversalEvent(self):
        response = self.publish(
            self.folder_path + '/@@switchDefaultSkin?skin_name=Plone%20Default',
            basic=self.basic_auth)
        self.assertEqual(response.getStatus(), 302)
        self.assertEqual(self.folder.absolute_url(),
                         response.getHeader("Location"))

        # Create new skin based on Plone Default and make this the
        # default skin.
        new_default_skin(self.portal)
        self.assertEqual("Monty Python Skin", self.folder.getCurrentSkinName())

        request = TestRequest(SERVER_URL='http://localhost')
        event = FakeTraversalEvent(self.folder, request)
        switch_skin(self.folder, event)
        self.assertEqual("Plone Default", self.folder.getCurrentSkinName())
        self.assertEqual(0, request.get("editskinswitched", 0))

    def testSkinSwitchedOnRealTraversalEvent(self):
        # Create new skin based on Plone Default and make this the
        # default skin.
        new_default_skin(self.portal)
        response = self.publish(
            self.folder_path + '/getCurrentSkinName',
            basic=self.basic_auth)
        self.assertEqual("Monty Python Skin", response.getBody())

        response = self.publish(
            self.folder_path + '/@@switchDefaultSkin?skin_name=Plone%20Default',
            basic=self.basic_auth)
        self.assertEqual(response.getStatus(), 302)
        self.assertEqual(self.folder.absolute_url(),
                         response.getHeader("Location"))

        response = self.publish(
            self.folder_path + '/getCurrentSkinName',
            basic=self.basic_auth)
        self.assertEqual("Plone Default", response.getBody())
