from zope.publisher.browser import BrowserPage
from upcnet.cas import util


class LoginUrl(BrowserPage):

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):
        return util.login_URL(self.context, self.request)


class LoginFormUrl(BrowserPage):

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):
        return util.loginForm_URL(self.context, self.request)


class Logout(BrowserPage):

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):
        util.logout(self.context, self.request)


class caslogin(BrowserPage):

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):

        portal = self.context.portal_url.getPortalObject()
        plugin = portal.acl_users.CASUPC

        if plugin.casServerUrlPrefix:
            url = plugin.getLoginURL() + '?service=' + plugin.getService().replace('/caslogin%3F', '')
            if plugin.renew:
                url += '&renew=true'
            if plugin.gateway:
                url += '&gateway=true'

            return self.request.RESPONSE.redirect(url, lock=1)


class caslogout(BrowserPage):

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):

        portal = self.context.portal_url.getPortalObject()
        cas_client_plugin = portal.acl_users.CASUPC

        mt = self.context.portal_membership
        mt.logoutUser(REQUEST=self.request)

        self.request.RESPONSE.redirect(cas_client_plugin.casServerUrlPrefix + '/logout')
