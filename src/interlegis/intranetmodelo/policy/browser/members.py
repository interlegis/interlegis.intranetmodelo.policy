# -*- coding: utf-8 -*-
from five import grok
from plone import api
from Products.CMFCore.interfaces import IFolderish

grok.templatedir('templates')


class MembersListView(grok.View):

    """List all members in the portal."""

    grok.context(IFolderish)
    grok.name('members-list')
    grok.require('zope2.Public')
    grok.template('members_list_view')

    def members(self):
        """Return a list of members.

        :returns: list of members
        :rtype: list of MemberData objects
        """
        portal_url = api.portal.get().absolute_url()
        results = api.user.get_users()
        members = []
        for u in results:
            members.append(dict(
                url=portal_url + '/author/' + u.id,
                portrait_url=self.get_portrait_url(u.id),
                fullname=u.getProperty('fullname'),
                description=u.getProperty('description'),
                extension=u.getProperty('extension'),
                mobile=u.getProperty('mobile'),
                location=u.getProperty('location'),
                email=u.getProperty('email'),
            ))
        return members

    def get_portrait_url(self, userid):
        """Return the URL of the portrait on a user profile.

        :param userid: [required] Userid of the user we want to get the
            portrait URL.
        :type userid: string
        :returns: URL to user portrait
        :rtype: string
        """
        membership = api.portal.get_tool('portal_membership')
        portrait = membership.getPersonalPortrait(userid)
        return portrait.absolute_url()
