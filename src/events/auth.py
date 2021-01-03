import logging

from ..services import AccountService, AddressService


class Auth:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.account_service = AccountService()
        self.address_service = AddressService()

    def handle_event(self, key, data):
        if key == 'auth_created':
            self.logger.info('auth created')
            address = self.address_service.create(country=data['country'])
            _ = self.account_service.create(user_uuid=data['uuid'], username=data['username'],
                                            email=data['email'], display_name=data['display_name'], status='active',
                                            role='member', address=address)
