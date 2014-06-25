# -*- coding: utf-8 -*-
from interlegis.intranetmodelo.policy.testing import INTEGRATION_TESTING
from plone.app.discussion.interfaces import IDiscussionSettings
from plone.registry.interfaces import IRegistry
from zope.component import getUtility

import unittest


class DiscussionTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.workflow = self.portal['portal_workflow']

    def test_configuration(self):
        settings = getUtility(IRegistry).forInterface(IDiscussionSettings)
        self.assertTrue(settings.anonymous_comments)
        self.assertTrue(settings.anonymous_email_enabled)
        self.assertEqual(settings.captcha, u'captcha')
        self.assertTrue(settings.globally_enabled)
        self.assertFalse(settings.moderation_enabled)
        self.assertTrue(settings.show_commenter_image)
        self.assertEqual(settings.text_transform, u'text/plain')

    def test_workflow(self):
        self.assertIn('comment_review_workflow', self.portal.portal_workflow)
        chain = self.workflow.getChainForPortalType('Discussion Item')
        self.assertEqual(chain, ('one_state_workflow',))

    def test_news_items_have_discussion_enabled(self):
        news_item = self.portal['portal_types']['News Item']
        self.assertTrue(news_item.allow_discussion)
