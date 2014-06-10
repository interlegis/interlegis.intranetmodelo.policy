# -*- coding: utf-8 -*-
from interlegis.intranetmodelo.policy.testing import INTEGRATION_TESTING
from plone import api
from plone.app.testing.interfaces import TEST_USER_ID

import unittest

FIELDS = [
    'birthday',
    'extension',
    'mobile',
]


class MembershipPropertiesTestCase(unittest.TestCase):

    """Ensure membership properties are properly installed."""

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']

    def test_memberdata_properties(self):
        memberdata = self.portal['portal_memberdata']
        for f in FIELDS:
            self.assertTrue(
                memberdata.hasProperty(f), 'not found: {0}'.format(f))

    def test_user_registration_fields(self):
        site_properties = self.portal['portal_properties'].site_properties
        user_registration_fields = site_properties.user_registration_fields
        for f in FIELDS:
            self.assertIn(
                f, user_registration_fields, 'not found: {0}'.format(f))


class MembersViewTestCase(unittest.TestCase):

    """Ensure membership view methods work as expected."""

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        self.view = api.content.get_view(
            name='members-list', context=self.portal, request=self.request)

    def test_members(self):
        members = self.view.members()
        self.assertEqual(len(members), 1)
        self.assertEqual(members[0]['fullname'], '')
        self.assertEqual(
            members[0]['url'], 'http://nohost/plone/author/test_user_1_')

    def test_get_portrait_url(self):
        portrait_url = self.view.get_portrait_url(TEST_USER_ID)
        self.assertEqual(portrait_url, 'http://nohost/plone/defaultUser.png')
