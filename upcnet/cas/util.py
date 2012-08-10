from Products.CMFCore.utils import getToolByName
from zExceptions import NotFound
from urllib import quote
from Products.statusmessages.interfaces import IStatusMessage
from Products.CMFPlone import PloneMessageFactory as _
from zope.component import getMultiAdapter
from Products.CMFCore.utils import getToolByName
from plone.memoize.instance import memoize


def login_URL(context, request):
    """ Refactored to use anz.casclient """
    # We suppose that a configured plugin is in place and its called CASUPC
    portal = getToolByName(context, "portal_url").getPortalObject()
    plugin = portal.acl_users.CASUPC
    # import ipdb;ipdb.set_trace()
    url = plugin.getLoginURL() + '?service=' + plugin.getService()
    if plugin.renew:
        url += '&renew=true'
    if plugin.gateway:
        url += '&gateway=true'

    return url


#REVIEW IF NEEDED after using anz.casclient


def URL(context):
    return context.restrictedTraverse('@@plone').getCurrentUrl()


def current2HTTPS(context, request):
        context_state = getMultiAdapter((context, request), name=u'plone_context_state')
        current_page = context_state.current_page_url()
        current_page_split = current_page.split(":")

        if len(current_page_split) > 0:
            if current_page_split[0] == 'http':
                current_page = current_page.replace('http', 'https')

        return current_page


def portal2HTTPS(context, request):
        context_state = getMultiAdapter((context, request), name=u'plone_portal_state')
        portalurl = context_state.portal_url()
        current_page_split = portalurl.split(":")

        if len(current_page_split) > 0:
            if current_page_split[0] == 'http':
                portalurl = portalurl.replace('http', 'https')

        return portalurl


def camefrom2HTTPS(camefrom):
        current_page_split = camefrom.split(":")

        if len(current_page_split) > 0:
            if current_page_split[0] == 'http':
                camefrom = camefrom.replace('http', 'https')

        return camefrom


def loginForm_query_string(context, request):
    """ Usat nomes en el login form """
    camefrom = getattr(request, 'came_from', '')
    camefrom = camefrom2HTTPS(camefrom)
    querystring = '?came_from=%s' % camefrom
    portalurl = portal2HTTPS(context, request)
    service_URL = ('%s/logged_in%s' % (portalurl, querystring))

    return '?service=%s' % (service_URL)


def loginForm_URL(context, request):
    """ Usat nomes en el login form """
    base = login_URL_base(context)

    if base is None:
        loginform = 'login_form'
        return loginform

    return '%s%s' % (base, loginForm_query_string(context, request))


def logout_URL_base(context):
    acl_users = getToolByName(context, 'acl_users')
    cas_auth_helpers = acl_users.objectValues(['CAS Auth Helper'])

    if cas_auth_helpers:
        return cas_auth_helpers[0].logout_url
    else:
        return None


def logout_URL(context):
    """ Enllac per fer logout """
    portalurl = getToolByName(context, 'portal_url').getPortalObject().absolute_url()
    base = logout_URL_base(context)

    return '%s?url=%s' % (base, portalurl)


def logout(context, request):
    mt = getToolByName(context, 'portal_membership')
    mt.logoutUser(REQUEST=request)
    IStatusMessage(request).addStatusMessage(_('heading_signed_out'), type='info')

    return request.RESPONSE.redirect(logout_URL(context))
