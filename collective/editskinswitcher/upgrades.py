import logging
from Products.CMFCore.utils import getToolByName
PROFILE_ID = 'profile-collective.editskinswitcher:default'


def add_property(sheet, propname, default, prop_type, logger):
    """Add property to the sheet, if it is not there yet.
    """
    if not sheet.hasProperty(propname):
        sheet._setProperty(propname, default, prop_type)
        logger.info('Added %s property %r with default value %r',
                    prop_type, propname, default)


def add_admin_header_property(context, logger=None):
    """Add the admin_header property.

    @parameters:

    When called from an 'import_various' method, 'context' will be
    the plone site and 'logger' is the portal_setup logger.  But
    this method can also be used as upgrade step, in which case
    'context' will be portal_setup and 'logger' will be None.
    """
    if logger is None:
        # Called as upgrade step: define our own logger.
        logger = logging.getLogger('collective.editskinswitcher')

    portal_props = getToolByName(context, 'portal_properties')
    sheet = portal_props.editskin_switcher
    add_property(sheet, 'admin_header', 'HTTP_PLONEADMIN', 'string', logger)


def add_force_login_header_property(context, logger=None):
    """Add the force_login_header property.
    """
    if logger is None:
        # Called as upgrade step: define our own logger.
        logger = logging.getLogger('collective.editskinswitcher')

    portal_props = getToolByName(context, 'portal_properties')
    sheet = portal_props.editskin_switcher
    add_property(sheet, 'force_login_header', 'FORCE_LOGIN', 'string', logger)