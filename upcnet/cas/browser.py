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