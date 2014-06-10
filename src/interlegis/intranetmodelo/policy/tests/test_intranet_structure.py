# -*- coding: utf-8 -*-
from interlegis.intranetmodelo.policy.config import INTRANET_STRUCTURE
from interlegis.intranetmodelo.policy.config import PROJECTNAME
from interlegis.intranetmodelo.policy.testing import INTEGRATION_TESTING
from plone import api
from plone.app.layout.navigation.interfaces import INavigationRoot
from plonesocial.microblog.interfaces import IMicroblogContext

import unittest


class IntranetStructureTestCase(unittest.TestCase):
    """Ensure intranet structure is created and configured.
    """

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.qi = self.portal['portal_quickinstaller']

    def test_intranet_folder_was_created(self):
        self.assertIn('intranet', self.portal)

    def test_intranet_folder_state_is_internal_draft(self):
        intranet = self.portal['intranet']
        self.assertEqual(api.content.get_state(intranet), 'internal')

    def test_intranet_structure_was_created(self):
        intranet = self.portal['intranet']
        for item in INTRANET_STRUCTURE:
            id = item['id']
            self.assertIn(id, intranet, u'{0} not created'.format(id))
            if '_children' in item:
                for child in item['_children']:
                    _id = child['id']
                    self.assertIn(
                        _id,
                        intranet[id],
                        u'{0}/{1} not created'.format(id, _id)
                    )

    def test_intranet_default_page(self):
        intranet = self.portal['intranet']
        self.assertEqual(
            intranet.getDefaultPage(), 'pagina-inicial-da-intranet')

    def test_intranet_navigation_root_context(self):
        intranet = self.portal['intranet']
        self.assertTrue(INavigationRoot.providedBy(intranet))

    def test_intranet_microblog_context(self):
        intranet = self.portal['intranet']
        self.assertTrue(IMicroblogContext.providedBy(intranet))

    def test_intranet_navigation_root_context_removed(self):
        self.qi.uninstallProducts(products=[PROJECTNAME])
        intranet = self.portal['intranet']
        self.assertFalse(INavigationRoot.providedBy(intranet))

    def test_intranet_microblog_context_removed(self):
        self.qi.uninstallProducts(products=[PROJECTNAME])
        intranet = self.portal['intranet']
        self.assertFalse(IMicroblogContext.providedBy(intranet))

    def test_intranet_setores_add_department(self):
        permission = 'interlegis.intranetmodelo.departments: Add Department'
        pm = api.portal.get_tool('portal_membership')
        check_permission = pm.checkPermission
        with api.env.adopt_roles(['Manager', ]):
            # Not allowed on intranet root
            intranet = self.portal['intranet']
            self.assertFalse(check_permission(permission, intranet))
            # Allowed on setores
            setores = intranet['setores']
            self.assertTrue(check_permission(permission, setores))

    def test_feedback_poll_is_open(self):
        intranet = self.portal['intranet']
        poll = intranet['institucional']['enquetes']['gostou-da-nova-intranet']
        self.assertEqual(api.content.get_state(poll), 'open')
