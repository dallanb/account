from .v1 import AccountsAPI, AccountsListAPI, AccountsListBulkAPI, AccountsMembershipAPI
from .v1 import PingAPI
from .. import api

# Ping
api.add_resource(PingAPI, '/ping', methods=['GET'])

# Accounts
api.add_resource(AccountsAPI, '/accounts/<uuid>', endpoint="account")
api.add_resource(AccountsListAPI, '/accounts', endpoint="accounts")
api.add_resource(AccountsListBulkAPI, '/accounts/bulk', endpoint="accounts_bulk")
api.add_resource(AccountsMembershipAPI, '/accounts/membership/<uuid>', endpoint="account_membership")
