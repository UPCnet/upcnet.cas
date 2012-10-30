from zope.component import queryUtility
from Products.CMFCore.utils import getToolByName
from plone.registry.interfaces import IRegistry
from anz.casclient.casclient import manage_addAnzCASClient
from upcnet.cas.interface import ICASSettings


def setupVarious(context):

    # Ordinarily, GenericSetup handlers check for the existence of XML files.
    # Here, we are not parsing an XML file, but we use this text file as a
    # flag to check that we actually meant for this import step to be run.
    # The file is found in profiles/default.

    if context.readDataFile('upcnet.cas_various.txt') is None:
        return

    portal = context.getSite()

    # Try to delete a possible existing instance of CASUPC object.
    try:
        portal.acl_users.manage_delObjects('CASUPC')
    except:
        pass
    try:
        manage_addAnzCASClient(portal.acl_users, "CASUPC", title="CASUPC")
        portal.acl_users.CASUPC.casServerUrlPrefix = 'https://cas.upc.edu'
        # portal.acl_users.CASUPC.gateway = True
        portal.acl_users.CASUPC.ticketValidationSpecification = 'CAS 2.0'
        plugin = portal.acl_users['CASUPC']
        plugin.manage_activateInterfaces(['IAuthenticationPlugin', 'IChallengePlugin', 'IExtractionPlugin'])
    except:
        pass

    # Try to migrate the existing App descriptor for CAS login page.
    try:
        genweb_props = getToolByName(context, 'portal_properties').genwebupc_properties
        registry = queryUtility(IRegistry)
        cas_settings = registry.forInterface(ICASSettings)
        cas_settings.cas_app_name = genweb_props.CASAuthAppName
    except:
        pass
