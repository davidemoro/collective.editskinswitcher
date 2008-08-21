### Event handler that modifies skins and actions tools based on the
### editskinswitcher property sheet - Ed Crewe

from Products.CMFCore.utils import getToolByName
from collective.editskinswitcher.browser.interfaces import IPropertiesModifiedEvent
from Products.CMFCore.DirectoryView import manage_addDirectoryView
from collective.editskinswitcher import monkeypatches

def skintabChange(sheet):
    ''' This toggles the preview tab and making view like preview '''
    preview = sheet.getProperty('add_preview_tab',False)
    a_tool = getToolByName(sheet, 'portal_actions')
    ptabs = getattr(a_tool,'object',None)
    if ptabs:
        prevtab = getattr(ptabs,'skinpreview',None)
        if prevtab:
            prevtab.visible = preview
        else:
            raise 'Sorry no skin preview tab found in object actions'
    else:
        raise 'Sorry no portal actions tool - object actions found'

    changeview = sheet.getProperty('change_view_into_preview',False)
    sk_tool = getToolByName(sheet, 'portal_skins')
    defaultpath = sk_tool.getSkinPath('Plone Default')
    changed = defaultpath.find('editskinswitcher_content') > -1
    if changeview != changed:
        sk_tool.manage_skinLayers( chosen=['Plone Default'], del_skin=1)
        if changeview and not changed:
            if not getattr(sk_tool,'editskinswitcher_content',None):
                addDir = sk_tool.manage_addProduct['CMFCore'].manage_addDirectoryView
                addDir(reg_key='collective.editskinswitcher:skins/editskinswitcher_content',id='editskinswitcher_content')
            skinpath = 'editskinswitcher_content,' + defaultpath
        elif not changeview and changed:
            skinpath = defaultpath.replace('editskinswitcher_content,','')
        sk_tool.addSkinSelection('Plone Default', skinpath)

### Create event handlers ... registered via configure.zcml

def propertiesEditedHandler(event):
    ''' Make edited properties have an immediate effect '''
    sheet = event.context
    if sheet.getId() == 'editskin_switcher':
        skintabChange(sheet)        

