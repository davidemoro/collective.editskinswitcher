from Products.CMFCore.permissions import setDefaultRoles

SetDefaultSkin = "SetDefaultSkin"

def initialize():
    """Initialize permission to role mappings."""
    setDefaultRoles(SetDefaultSkin, ('Manager', 'Owner'))
