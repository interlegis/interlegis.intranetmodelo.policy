# -*- coding: utf-8 -*-
from interlegis.intranetmodelo.policy.config import DEPENDENCIES as ZOPE2_STYLE_PRODUCTS
from interlegis.intranetmodelo.policy.config import PROJECTNAME
from interlegis.intranetmodelo.policy.interfaces import IBrowserLayer
from interlegis.intranetmodelo.policy.testing import INTEGRATION_TESTING
from plone.browserlayer.utils import registered_layers
from plone.registry.interfaces import IRegistry
from zope.component import getUtility

import unittest

# these packages must be available, but not installed
AVAILABLE = [
    'collective.xmpp.chat',
    'collective.xmpp.core',
    'plone.app.ldap',
    'plone.app.openid',
    'webcouturier.dropdownmenu',
]

DEPENDENCIES = [
    'cioppino.twothumbs',
    'collective.classifieds',
    'collective.cover',
    'collective.polls',
    # 'collective.xmpp.chat',
    # 'collective.xmpp.core',
    'collective.weather',
    'ftw.globalstatusmessage',
    'interlegis.intranetmodelo.departments',
    'plone.app.event',
    'plonesocial.activitystream',
    'plonesocial.microblog',
    'plonesocial.network',
    's17.portlets',
    's17.taskmanager',
    'Solgema.fullcalendar',
] + ZOPE2_STYLE_PRODUCTS


class BaseTestCase(unittest.TestCase):
    """Base test case to be used by other tests."""

    layer = INTEGRATION_TESTING

    profile = 'interlegis.intranetmodelo.policy:default'

    def setUp(self):
        self.portal = self.layer['portal']
        self.qi = self.portal['portal_quickinstaller']
        self.wt = self.portal['portal_workflow']
        self.st = self.portal['portal_setup']


class InstallTestCase(BaseTestCase):
    """Ensure product is properly installed."""

    def test_installed(self):
        self.assertTrue(self.qi.isProductInstalled(PROJECTNAME))

    def test_dependencies_installed(self):
        for i in DEPENDENCIES:
            self.assertTrue(
                self.qi.isProductInstalled(i), u'{0} not installed'.format(i))

    def test_available_packages(self):
        for i in AVAILABLE:
            self.assertIn(i, self.qi.listInstallableProfiles())

    def test_browser_layer_installed(self):
        self.assertIn(IBrowserLayer, registered_layers())


class UninstallTestCase(BaseTestCase):
    """Ensure product is properly uninstalled."""

    def test_uninstalled(self):
        self.qi.uninstallProducts(products=[PROJECTNAME])
        self.assertFalse(self.qi.isProductInstalled(PROJECTNAME))

    def test_browser_layer_removed(self):
        self.assertNotIn(IBrowserLayer, registered_layers())


class DependenciesSettingsTestCase(unittest.TestCase):
    """Ensure package dependencies are properly configured."""

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.registry = getUtility(IRegistry)

    def test_collective_cover_settings(self):
        from collective.cover.controlpanel import ICoverSettings
        settings = self.registry.forInterface(ICoverSettings)
        self.assertEqual(len(settings.layouts), 5)
        self.assertIn(u'Intranet Modelo', settings.layouts)

    def test_plone_app_event_settings(self):
        self.assertEqual(
            self.registry['plone.app.event.portal_timezone'], u'Brazil/East')
        self.assertListEqual(
            self.registry['plone.app.event.available_timezones'],
            [u'Brazil/Acre', u'Brazil/DeNoronha', u'Brazil/East', u'Brazil/West']
        )
        self.assertEqual(self.registry['plone.app.event.first_weekday'], u'6')

    def test_collective_weather_settings(self):
        from collective.weather.interfaces import IWeatherSettings
        settings = self.registry.forInterface(IWeatherSettings)
        expected = [u'455819|Brasília, DF']
        self.assertEqual(settings.location_ids, expected)
