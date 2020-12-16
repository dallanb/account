import logging

from ..services import AccountService


class Auth:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.account_service = AccountService()

    def handle_event(self, key, data):
        if key == 'auth_created':
            self.logger.info('auth created')
            _ = self.account_service.create(membership_uuid=data['uuid'], username=data['username'],
                                            email=data['email'], first_name=data['first_name'],
                                            last_name=data['last_name'], status='active',
                                            role='member')
