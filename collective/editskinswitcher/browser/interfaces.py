from plone.theme.interfaces import IDefaultPloneLayer
from zope.interface import Interface, Attribute, implements
from zope.viewlet.interfaces import IViewletManager

# New content type interfaces

class IThemeSpecific(IDefaultPloneLayer):
    """Marker interface that defines a Zope 3 browser layer.
       If you need to register a view only for the
       editskinswitcher, this interface must be its layer
    """

class IPreviewView(Interface):
    """ A separate preview page for an object
        It displays it as it appears in one skin for viewing within a different (edit) skin """

class IPreviewViewlet(Interface):
    """ A preview viewlet for replacing the default view content body
        It displays an object as it appears in one skin for viewing within a different (edit) skin """

class IContentBodyViewletManager(IViewletManager):
    """A viewlet manager that replaces the normal content body of the page
    """

### We want to do things based on changing the property sheet
### Since this doesn't trigger a zope.lifecycleevent.ObjectModifiedEvent 
### we need to manually add an event which is monkeypatched into the TTW edit properties method

# create property modified event interface

class IPropertiesModifiedEvent(Interface):
    """An event for firing when a property sheet is saved. """
    context = Attribute("The properties have been saved.")

# create property modified event

class PropertiesModifiedEvent(object):
    """Event to notify that a property sheet has been saved. """
    implements(IPropertiesModifiedEvent)
    def __init__(self, context):
        self.context = context
