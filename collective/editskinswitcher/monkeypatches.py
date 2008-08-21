### Add event to saving property sheets  ... via monkeypatch :-( ... yuck
### We should probably drop the use of a property sheet and add a portal control panel to do this instead

### NB: This just makes sure changing the properties immediately has an effect for ZMI and testing purposes
### ... if you are happy to just set up the configuration via your default skin theme egg profile files 
### you can comment out this files import in edit_properties.py 
### ... however you will now need to add a python script to the portal with id editSwitchList returning the properties below

from collective.editskinswitcher.browser.interfaces import PropertiesModifiedEvent
from zope.event import notify
from Products.CMFPlone.PropertiesTool import SimpleItemWithProperties
from Globals import InitializeClass

def manage_editProperties(self, REQUEST):
    """Edit object properties via the web.
       ... add properties modified event notification
    """
    for prop in self._propertyMap():
        name=prop['id']
        if 'w' in prop.get('mode', 'wd'):
            if prop['type'] == 'multiple selection':
                value=REQUEST.get(name, [])
            else:
                value=REQUEST.get(name, '')
            self._updateProperty(name, value)

    notify(PropertiesModifiedEvent(self))

    if REQUEST:
        message="Saved changes."
        return self.manage_propertiesForm(self,REQUEST,
                                          manage_tabs_message=message)

def editSwitchList(self):
    """ Options for switch_skin_action property """
    return ["based on edit URL","based on specific domains","based on SSL","no URL based switching"]

setattr(SimpleItemWithProperties,'manage_editProperties',manage_editProperties)
setattr(SimpleItemWithProperties,'editSwitchList',editSwitchList)
InitializeClass(SimpleItemWithProperties)

