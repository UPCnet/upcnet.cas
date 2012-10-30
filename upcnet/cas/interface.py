# -*- coding: utf-8 -*-
from zope import schema
from plone.supermodel import model

try:
    from genweb.core import GenwebMessageFactory as _
except ImportError:
    from upcnet.cas import CASMessageFactory as _


class ICASSettings(model.Schema):
    """ Global CAS settings. This describes records stored in the
    configuration registry and obtainable via plone.registry.
    """

    cas_app_name = schema.TextLine(
        title=_(u"cas_app_name",
                default=u"Desciptor de l'aplicació"),
        description=_(u"help_cas_app_name",
                default=u"El descriptor per la personalització de l'aplicació per la pantalla de login de CAS"),
        required=False,
        default=u"genweb",
        )
