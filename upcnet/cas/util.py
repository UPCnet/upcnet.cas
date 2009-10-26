from Products.CMFCore.utils import getToolByName
from zExceptions import NotFound
from urllib import quote
from Products.statusmessages.interfaces import IStatusMessage
from Products.CMFPlone import PloneMessageFactory as _
from zope.component import getMultiAdapter

def URL(context):
    return context.restrictedTraverse('@@plone').getCurrentUrl()

def current2HTTPS(context, request):
        context_state = getMultiAdapter((context, request), name=u'plone_context_state')
        current_page = context_state.current_page_url()
        current_page_split = current_page.split(":")
        if len(current_page_split)>0:
            if current_page_split[0]=='http':
                current_page = current_page.replace('http','https')
        return current_page

def portal2HTTPS(context, request):
        context_state = getMultiAdapter((context, request), name=u'plone_portal_state')
        portalurl = context_state.portal_url()
        current_page_split = portalurl.split(":")
        if len(current_page_split)>0:
            if current_page_split[0]=='http':
                portalurl = portalurl.replace('http','https')
        return portalurl

def login_URL_base(context):
    acl_users = getToolByName(context, 'acl_users')
    cas_auth_helpers = acl_users.objectValues(['CAS Auth Helper'])
    if cas_auth_helpers:
        return cas_auth_helpers[0].getLoginURL()
    else:
        return None

def login_query_string(context, request): 
    #quoted_here_url = mtool = quote(URL(context), '')
    querystring = '?came_from=%s' % current2HTTPS(context, request)
    portalurl = portal2HTTPS(context, request)
    #portalurl = getToolByName(context, 'portal_url').getPortalObject().absolute_url()
    #portal = URL(getToolByName(context, 'portal_url').getPortalObject())
    if portalurl[-1:] == '/':
        portalurl = portalurl[:-1]
    service_URL =('%s/logged_in%s' % (portalurl, querystring))
    return '?service=%s&idApp=genweb' % service_URL

def login_URL(context, request):
    base = login_URL_base(context)
    if base is None:
        #loginform = getToolByName(context, 'portal_url').getPortalObject().absolute_url() + '/login_form'
        loginform = 'login_form'
        return loginform
    return '%s%s' % (base, login_query_string(context, request))


def loginForm_query_string(context,request):
    """ Usat nomes en el login form """
    querystring = '?came_from=%s' % getattr(request, 'came_from','')
    #portalurl = getToolByName(context, 'portal_url').getPortalObject().absolute_url()
    portalurl = portal2HTTPS(context, request)
    service_URL =('%s/logged_in%s' % (portalurl, querystring))
    return '?service=%s&idApp=genweb' % service_URL

def loginForm_URL(context, request):
    """ Usat nomes en el login form """
    #portal = URL(getToolByName(context, 'portal_url').getPortalObject())
    #portalurl = portal2HTTPS(context, request)
    base = login_URL_base(context)
    if base is None:
        #loginform = getToolByName(context, 'portal_url').getPortalObject().absolute_url() + '/login_form'
        loginform = 'login_form'
        return loginform
    return '%s%s' % (base, loginForm_query_string(context,request))

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

