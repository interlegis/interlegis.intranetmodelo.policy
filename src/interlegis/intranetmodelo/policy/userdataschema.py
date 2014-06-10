# -*- coding: utf-8 -*-
from datetime import datetime
from interlegis.intranetmodelo.policy import _
from plone.app.users.userdataschema import IUserDataSchema
from plone.app.users.userdataschema import IUserDataSchemaProvider
from zope import schema
from zope.interface import implements
from zope.schema import ValidationError


class DateInvalid(ValidationError):
    __doc__ = _(u'Invalid date format.')


def check_date(value):
    try:
        datetime.strptime(value, '%d/%m/%Y')
        return True
    except ValueError:
        raise DateInvalid  # the string does not match format


class UserDataSchemaProvider(object):
    implements(IUserDataSchemaProvider)

    def getSchema(self):
        return IEnhancedUserDataSchema


class IEnhancedUserDataSchema(IUserDataSchema):

    """Use all the fields from the default user data schema, and add various
    extra fields.
    """

    birthday = schema.ASCIILine(
        title=_(u'label_birthday', default=u'Birthday'),
        description=_(
            u'help_birthday',
            default=u'Your date of birth, in the format dd/mm/yyyy.'
        ),
        required=False,
        constraint=check_date,
    )

    extension = schema.ASCIILine(
        title=_(u'label_extension', default=u'Extension'),
        description=_(
            u'help_extension',
            default=u'Extension number, in xxxx format.'
        ),
        required=False,
    )

    mobile = schema.ASCIILine(
        title=_(u'label_mobile', default=u'Mobile'),
        description=_(
            u'help_mobile',
            default=u'Your mobile phone number, in xxxx-xxxx format.'
        ),
        required=False,
    )
