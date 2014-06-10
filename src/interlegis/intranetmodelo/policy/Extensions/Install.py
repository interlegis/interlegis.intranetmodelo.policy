# -*- coding: utf-8 -*-
from plone.app.layout.navigation.interfaces import INavigationRoot
from plonesocial.microblog.interfaces import IMicroblogContext
from zope.interface import noLongerProvides


def uninstall(portal, reinstall=False):
    if not reinstall:
        if 'intranet' in portal:
            intranet = portal['intranet']
            # do not leave broken marker interfaces behind
            if INavigationRoot.providedBy(intranet):
                noLongerProvides(intranet, INavigationRoot)
            if IMicroblogContext.providedBy(intranet):
                noLongerProvides(intranet, IMicroblogContext)
        return 'Ran all uninstall steps.'
