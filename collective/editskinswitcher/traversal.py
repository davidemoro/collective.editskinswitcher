from AccessControl import Unauthorized
from Products.CMFCore.utils import getToolByName


def check_auth(request):
    if not request.cookies.get('__ac'):
        raise Unauthorized('Go away')


def edit_url(request, props):
    ''' The default switch check based on a subdomain of cms, edit or manage'''
    from collective.editskinswitcher.utils import is_edit_url
    return is_edit_url(request.getURL())


def specific_domain(request, props):
    specific_domains = props.getProperty('specific_domains', ())
    if specific_domains != ():
        thisurl = request.getURL()
        if thisurl in specific_domains:
            return True
    return False


def ssl_url(request, props):
    parts = request.getURL().split('://')
    if parts[0]=='https':
        return True
    return False


def force_login(request, props):
    force_login_header = props.getProperty('force_login_header', None)
    if not force_login_header:
        return False
    if request.get(force_login_header, None):
        return True
    return False


def admin_header(request, props):
    admin_header = props.getProperty('admin_header', 'HTTP_PLONEADMIN')
    if request.get(admin_header, None):
        return True
    return False


def no_url(request, props):
    """This is for skin switching based on authentication only."""
    return props.getProperty('need_authentication', False)


methods = {'based on edit URL': edit_url,
           'based on specific domains': specific_domain,
           'based on SSL': ssl_url,
           'based on admin header': admin_header,           
           'no URL based switching': no_url}


def switch_skin(object, event):
    """Switch to the Plone Default skin when we are editing.
    """
    request = event.request
    portal_props = getToolByName(object, 'portal_properties', None)
    if portal_props is None:
        return None
    editskin_props = portal_props.get('editskin_switcher')
    if editskin_props is None:
        return None

    # Okay, we have a property sheet we can use.
    edit_skin = editskin_props.getProperty('edit_skin', '')

    if force_login(request, editskin_props):
        # We have a header that forces us to be logged in; so add a
        # hook at the end of the traversal to check that we really are
        # logged in.
        request.post_traverse(check_auth, (request, ))

    # Check if we need authentication first, possibly in addition to
    # one of the other tests
    if editskin_props.getProperty('need_authentication', False) \
            and not request.cookies.get('__ac'):
        return None

    switch = editskin_props.getProperty('switch_skin_action',
                                        'based on edit URL')
    if not methods.get(switch, edit_url)(request, editskin_props):
        return None

    # Use to preview default skin in edit skin mode
    if request.get('mutate_skin', '') == 'default':
        return None

    # object might be a view, for instance a KSS view.  Use the
    # context of that object then.
    try:
        changeSkin = object.changeSkin
    except AttributeError:
        changeSkin = object.context.changeSkin

    # Assume that if you get here you are switching to the edit skin
    # ... flag this for the purposes of caching / kss loading etc.
    request.set('editskinswitched', 1)

    # If the edit_skin does not exist, the next call is
    # intelligent enough to use the default skin instead.
    changeSkin(edit_skin, request)
    return None
