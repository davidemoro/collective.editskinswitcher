from collective.editskinswitcher.tests import baselayers as base

class TestLayers(base.LayersTestCase):

    def test_layers_default_config(self):
        """ Test with default options (switch_skin_action = based on edit URL)"""
        portal = self.portal
        from collective.editskinswitcher.tests.interfaces import ILayerTest1
        from collective.editskinswitcher.tests.interfaces import ILayerTest2
        # the request should be marked with the ILayerTest1 but Plone testing
        # tool kits won't register layers for you.
        # See http://developer.plone.org/views/layers.html#testing-layers
        self.assertFalse(ILayerTest1 in portal.REQUEST.__provides__.__iro__)
        self.assertFalse(ILayerTest2 in portal.REQUEST.__provides__.__iro__)

        # Default theme: Layertest 1
        self.assertEquals('Layertest 1', portal.portal_skins.getDefaultSkin())

        # Fallback edit theme: Layertest 2
        from Products.CMFCore.utils import getToolByName
        portal_props = getToolByName(portal, 'portal_properties')
        editskin_props = portal_props.get('editskin_switcher')
        editskin_props.edit_skin = 'Layertest 2'

        from collective.editskinswitcher.tests.utils import TestRequest
        from collective.editskinswitcher.tests.utils import FakeTraversalEvent
        from collective.editskinswitcher.traversal import switch_skin
        request = TestRequest(SERVER_URL='http://localhost')
        portal.REQUEST = request
        event = FakeTraversalEvent(portal, request)
        switch_skin(portal, event)
        self.assertEquals('Layertest 1', portal.getCurrentSkinName())

        # no change skin, so add the ILayerTest1 manually for now since
        # Plone testing tool kits won't register layers for you
        from zope.interface import directlyProvides
        directlyProvides(portal.REQUEST, ILayerTest1)
        # After the switch_skin the ILayerTest1 should be active
        self.assertTrue(ILayerTest1 in portal.REQUEST.__provides__.__iro__)
        self.assertFalse(ILayerTest2 in portal.REQUEST.__provides__.__iro__)
        self.assertEquals('layer1\n', self.portal.restrictedTraverse('@@layer_view')())

        request = TestRequest(SERVER_URL='http://127.0.0.1')
        portal.REQUEST = request
        event = FakeTraversalEvent(portal, request)
        switch_skin(portal, event)
        self.assertEquals('Layertest 2', portal.getCurrentSkinName())

        # After the switch_skin the ILayerTest2 should be active
        self.assertFalse(ILayerTest1 in portal.REQUEST.__provides__.__iro__)
        self.assertTrue(ILayerTest2 in portal.REQUEST.__provides__.__iro__)
        self.assertEquals('layer2\n', self.portal.restrictedTraverse('@@layer_view')())

    def test_layers_specific_domains_1(self):
        """ Test with the specific_domains option with http://foobar.com"""
        portal = self.portal
        from collective.editskinswitcher.tests.interfaces import ILayerTest1
        from collective.editskinswitcher.tests.interfaces import ILayerTest2
        # the request should be marked with the ILayerTest1 but Plone testing
        # tool kits won't register layers for you.
        # See http://developer.plone.org/views/layers.html#testing-layers
        self.assertFalse(ILayerTest1 in portal.REQUEST.__provides__.__iro__)
        self.assertFalse(ILayerTest2 in portal.REQUEST.__provides__.__iro__)

        # Default theme: Layertest 1
        self.assertEquals('Layertest 1', portal.portal_skins.getDefaultSkin())

        # Fallback edit theme: Layertest 2
        from Products.CMFCore.utils import getToolByName
        portal_props = getToolByName(portal, 'portal_properties')
        editskin_props = portal_props.get('editskin_switcher')
        editskin_props.edit_skin = 'Layertest 2'
        editskin_props.specific_domains = 'http://foobar.com'
        editskin_props.switch_skin_action = 'based on specific domains'

        from collective.editskinswitcher.tests.utils import TestRequest
        from collective.editskinswitcher.tests.utils import FakeTraversalEvent
        from collective.editskinswitcher.traversal import switch_skin
        request = TestRequest(SERVER_URL='http://localhost')
        portal.REQUEST = request
        event = FakeTraversalEvent(portal, request)
        switch_skin(portal, event)
        self.assertEquals('Layertest 1', portal.getCurrentSkinName())

        # no change skin, so add the ILayerTest1 manually for now since
        # Plone testing tool kits won't register layers for you
        from zope.interface import directlyProvides
        directlyProvides(portal.REQUEST, ILayerTest1)
        # After the switch_skin the ILayerTest1 should be active
        self.assertTrue(ILayerTest1 in portal.REQUEST.__provides__.__iro__)
        self.assertFalse(ILayerTest2 in portal.REQUEST.__provides__.__iro__)
        self.assertEquals('layer1\n', self.portal.restrictedTraverse('@@layer_view')())

        request = TestRequest(SERVER_URL='http://foobar.com')
        portal.REQUEST = request
        event = FakeTraversalEvent(portal, request)
        switch_skin(portal, event)
        self.assertEquals('Layertest 2', portal.getCurrentSkinName())

        # After the switch_skin the ILayerTest2 should be active
        self.assertFalse(ILayerTest1 in portal.REQUEST.__provides__.__iro__)
        self.assertTrue(ILayerTest2 in portal.REQUEST.__provides__.__iro__)
        self.assertEquals('layer2\n', self.portal.restrictedTraverse('@@layer_view')())

    def test_layers_specific_domains_2(self):
        """ Test with the specific_domains option with http://edit.bar.com"""
        portal = self.portal
        from collective.editskinswitcher.tests.interfaces import ILayerTest1
        from collective.editskinswitcher.tests.interfaces import ILayerTest2
        # the request should be marked with the ILayerTest1 but Plone testing
        # tool kits won't register layers for you.
        # See http://developer.plone.org/views/layers.html#testing-layers
        self.assertFalse(ILayerTest1 in portal.REQUEST.__provides__.__iro__)
        self.assertFalse(ILayerTest2 in portal.REQUEST.__provides__.__iro__)

        # Default theme: Layertest 1
        self.assertEquals('Layertest 1', portal.portal_skins.getDefaultSkin())

        # Fallback edit theme: Layertest 2
        from Products.CMFCore.utils import getToolByName
        portal_props = getToolByName(portal, 'portal_properties')
        editskin_props = portal_props.get('editskin_switcher')
        editskin_props.edit_skin = 'Layertest 2'
        editskin_props.specific_domains = 'http://edit.bar.com'
        editskin_props.switch_skin_action = 'based on specific domains'

        from collective.editskinswitcher.tests.utils import TestRequest
        from collective.editskinswitcher.tests.utils import FakeTraversalEvent
        from collective.editskinswitcher.traversal import switch_skin
        request = TestRequest(SERVER_URL='http://localhost')
        portal.REQUEST = request
        event = FakeTraversalEvent(portal, request)
        switch_skin(portal, event)
        self.assertEquals('Layertest 1', portal.getCurrentSkinName())

        # no change skin, so add the ILayerTest1 manually for now since
        # Plone testing tool kits won't register layers for you
        from zope.interface import directlyProvides
        directlyProvides(portal.REQUEST, ILayerTest1)
        # After the switch_skin the ILayerTest1 should be active
        self.assertTrue(ILayerTest1 in portal.REQUEST.__provides__.__iro__)
        self.assertFalse(ILayerTest2 in portal.REQUEST.__provides__.__iro__)
        self.assertEquals('layer1\n', self.portal.restrictedTraverse('@@layer_view')())

        request = TestRequest(SERVER_URL='http://edit.bar.com')
        portal.REQUEST = request
        event = FakeTraversalEvent(portal, request)
        switch_skin(portal, event)
        self.assertEquals('Layertest 2', portal.getCurrentSkinName())

        # After the switch_skin the ILayerTest2 should be active
        self.assertFalse(ILayerTest1 in portal.REQUEST.__provides__.__iro__)
        self.assertTrue(ILayerTest2 in portal.REQUEST.__provides__.__iro__)
        self.assertEquals('layer2\n', self.portal.restrictedTraverse('@@layer_view')())

    def test_layers_specific_domains_3(self):
        """ Test with the specific_domains option with http://edit.bar.com/something"""
        portal = self.portal
        from collective.editskinswitcher.tests.interfaces import ILayerTest1
        from collective.editskinswitcher.tests.interfaces import ILayerTest2
        # the request should be marked with the ILayerTest1 but Plone testing
        # tool kits won't register layers for you.
        # See http://developer.plone.org/views/layers.html#testing-layers
        self.assertFalse(ILayerTest1 in portal.REQUEST.__provides__.__iro__)
        self.assertFalse(ILayerTest2 in portal.REQUEST.__provides__.__iro__)

        # Default theme: Layertest 1
        self.assertEquals('Layertest 1', portal.portal_skins.getDefaultSkin())

        # Fallback edit theme: Layertest 2
        from Products.CMFCore.utils import getToolByName
        portal_props = getToolByName(portal, 'portal_properties')
        editskin_props = portal_props.get('editskin_switcher')
        editskin_props.edit_skin = 'Layertest 2'
        editskin_props.specific_domains = 'http://edit.bar.com'
        editskin_props.switch_skin_action = 'based on specific domains'

        from collective.editskinswitcher.tests.utils import TestRequest
        from collective.editskinswitcher.tests.utils import FakeTraversalEvent
        from collective.editskinswitcher.traversal import switch_skin
        request = TestRequest(SERVER_URL='http://localhost')
        portal.REQUEST = request
        event = FakeTraversalEvent(portal, request)
        switch_skin(portal, event)
        self.assertEquals('Layertest 1', portal.getCurrentSkinName())

        # no change skin, so add the ILayerTest1 manually for now since
        # Plone testing tool kits won't register layers for you
        from zope.interface import directlyProvides
        directlyProvides(portal.REQUEST, ILayerTest1)
        # After the switch_skin the ILayerTest1 should be active
        self.assertTrue(ILayerTest1 in portal.REQUEST.__provides__.__iro__)
        self.assertFalse(ILayerTest2 in portal.REQUEST.__provides__.__iro__)
        self.assertEquals('layer1\n', self.portal.restrictedTraverse('@@layer_view')())

        request = TestRequest(SERVER_URL='http://edit.bar.com/something')
        portal.REQUEST = request
        event = FakeTraversalEvent(portal, request)
        switch_skin(portal, event)
        self.assertEquals('Layertest 2', portal.getCurrentSkinName())

        # After the switch_skin the ILayerTest2 should be active
        self.assertFalse(ILayerTest1 in portal.REQUEST.__provides__.__iro__)
        self.assertTrue(ILayerTest2 in portal.REQUEST.__provides__.__iro__)
        self.assertEquals('layer2\n', self.portal.restrictedTraverse('@@layer_view')())


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestLayers))
    return suite
