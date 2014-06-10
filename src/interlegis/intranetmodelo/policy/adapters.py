# -*- coding: utf-8 -*-
from plone.app.users.browser.personalpreferences import UserDataPanelAdapter


class EnhancedUserDataPanelAdapter(UserDataPanelAdapter):

    def get_birthday(self):
        return self.context.getProperty('birthday', '')

    def set_birthday(self, value):
        return self.context.setMemberProperties({'birthday': value})

    birthday = property(get_birthday, set_birthday)

    def get_extension(self):
        return self.context.getProperty('extension', '')

    def set_extension(self, value):
        return self.context.setMemberProperties({'extension': value})

    extension = property(get_extension, set_extension)

    def get_mobile(self):
        return self.context.getProperty('mobile', '')

    def set_mobile(self, value):
        return self.context.setMemberProperties({'mobile': value})

    mobile = property(get_mobile, set_mobile)
