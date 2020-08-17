from .. import api
from .v1 import PingAPI
from .v1 import AccountsAPI, AccountsListAPI

# Ping
api.add_resource(PingAPI, '/ping', methods=['GET'])

# Accounts
api.add_resource(AccountsAPI, '/accounts/<uuid:uuid>', endpoint="account")
api.add_resource(AccountsListAPI, '/accounts', endpoint="accounts")
