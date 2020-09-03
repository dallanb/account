from .v1 import AccountsAPI, AccountsListAPI
from .v1 import AvatarsAPI
from .v1 import MailAPI
from .v1 import PingAPI
from .. import api

# Ping
api.add_resource(PingAPI, '/ping', methods=['GET'])

# Accounts
api.add_resource(AccountsAPI, '/accounts/<uuid>', endpoint="account")
api.add_resource(AccountsListAPI, '/accounts', endpoint="accounts")

# Avatars
api.add_resource(AvatarsAPI, '/accounts/<uuid>/avatars', endpoint="avatar")

# Mail
api.add_resource(MailAPI, '/accounts/<uuid>/mail', endpoint="mail")