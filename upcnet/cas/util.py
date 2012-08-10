from Products.CMFCore.utils import getToolByName
from urllib import unquote
from Products.statusmessages.interfaces import IStatusMessage
from Products.CMFPlone import PloneMessageFactory as _


def secureURL(url):
    """ Secures an URL (given http, returns https) """
    if url[:5] == 'http:' or url[:5] == 'HTTP:':
        return '%s%s' % ('https:', url[5:])
    else:
        return url


def login_URL(context, request):
    """ Refactored to use anz.casclient """
    # We suppose that a configured plugin is in place and its called CASUPC
    portal = getToolByName(context, "portal_url").getPortalObject()
    plugin = portal.acl_users.CASUPC

    url = '%s%s%s' % (plugin.getLoginURL(), '?service=', secureURL(unquote(plugin.getService())))

    if plugin.renew:
        url += '&renew=true'
    if plugin.gateway:
        url += '&gateway=true'

    return url


def logout(context, request):
    portal = getToolByName(context, "portal_url").getPortalObject()
    plugin = portal.acl_users.CASUPC

    mt = getToolByName(context, 'portal_membership')
    mt.logoutUser(REQUEST=request)
    IStatusMessage(request).addStatusMessage(_('heading_signed_out'), type='info')

    logout_url = '%s%s%s' % (plugin.casServerUrlPrefix, '/logout?url=', portal.absolute_url())

    return request.RESPONSE.redirect(logout_url)


def loginForm_URL(context, request):
    """ Special treatment of the login_form CAS URL, otherwise the return URL
        will be the login form once authenticated. """
    camefrom = getattr(request, 'came_from', '')
    if not camefrom:
        camefrom = getToolByName(context, "portal_url").getPortalObject().absolute_url()

    # We suppose that a configured plugin is in place and its called CASUPC
    portal = getToolByName(context, "portal_url").getPortalObject()
    plugin = portal.acl_users.CASUPC

    url = '%s%s%s%s%s%s' % (plugin.getLoginURL(), '?service=', secureURL(portal.absolute_url()), '/logged_in?', 'came_from=', secureURL(camefrom))

    if plugin.renew:
        url += '&renew=true'
    if plugin.gateway:
        url += '&gateway=true'

    return url
