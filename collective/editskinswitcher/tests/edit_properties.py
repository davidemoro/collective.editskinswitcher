### Handler that modifies skins and actions tools 
from Products.CMFCore.utils import getToolByName
from Products.CMFCore.DirectoryView import manage_addDirectoryView

def skintabChange(props):
    ''' This toggles the preview tab and making view like preview '''
    preview = props.get('add_preview_tab',False)
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

    changeview = props.get('change_view_into_preview',False)
    sk_tool = getToolByName(sheet, 'portal_skins')
    defaultpath = sk_tool.getSkinPath('Plone Default')
    changed = defaultpath.find('editskinswitcher_edit_content') > -1
    if changeview != changed:
        sk_tool.manage_skinLayers( chosen=['Plone Default'], del_skin=1)
        if changeview and not changed:
            if not getattr(sk_tool,'editskinswitcher_edit_content',None):
                addDir = sk_tool.manage_addProduct['CMFCore'].manage_addDirectoryView
                addDir(reg_key='collective.editskinswitcher.tests:skins/editskinswitcher_edit_content',id='editskinswitcher_edit_content')
            skinpath = 'editskinswitcher_edit_content,' + defaultpath
        elif not changeview and changed:
            skinpath = defaultpath.replace('editskinswitcher_edit_content,','')
        sk_tool.addSkinSelection('Plone Default', skinpath)

