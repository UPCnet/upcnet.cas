from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import _createObjectByType

from collective.cas4plone.CASAuthHelper import addCASAuthHelper 

from plone.app.controlpanel.site import ISiteSchema

from zope.component import getAdapters

import transaction

def setupVarious(context):
    
    # Ordinarily, GenericSetup handlers check for the existence of XML files.
    # Here, we are not parsing an XML file, but we use this text file as a 
    # flag to check that we actually meant for this import step to be run.
    # The file is found in profiles/default.
    
    if context.readDataFile('upcnet.cas_various.txt') is None:
        return

    portal = context.getSite()
    try:
            addCASAuthHelper(portal.acl_users, "CASUPC", title="CASUPC")
            portal.acl_users.CASUPC.login_url='https://cas.upc.edu/login'
            portal.acl_users.CASUPC.logout_url='https://cas.upc.edu/logout'
            portal.acl_users.CASUPC.validate_url='https://cas.upc.edu/validate'
            plugin = portal.acl_users['CASUPC']
            plugin.manage_activateInterfaces(['IAuthenticationPlugin','IChallengePlugin','IExtractionPlugin'])

    except: 
            pass

