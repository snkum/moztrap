"""
User-related remote objects.

"""
from ..core.api import RemoteObject, ListObject, fields
from ..core.models import Company
from ..static.fields import StaticData


class User(RemoteObject):
    company = fields.Locator(Company)
    email = fields.Field()
    firstName = fields.Field()
    lastName = fields.Field()
    password = fields.Field()
    screenName = fields.Field()
    userStatus = StaticData("USERSTATUS")


    def __unicode__(self):
        return self.screenName


class UserList(ListObject):
    entryclass = User
    api_name = "users"
    default_url = "users"

    entries = fields.List(fields.Object(User))


    def __unicode__(self):
        return u"%s Users" % len(self)
