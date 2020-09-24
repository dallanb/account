import logging
from http import HTTPStatus

from .base import Base
from ..models import Account as AccountModel


class Account(Base):
    def __init__(self):
        Base.__init__(self)
        self.logger = logging.getLogger(__name__)
        self.account_model = AccountModel

    def find(self, **kwargs):
        return Base.find(self, model=self.account_model, **kwargs)

    def create(self, **kwargs):
        account = self.init(model=self.account_model, **kwargs)
        _ = self.notify(
            topic='accounts',
            value={'uuid': str(account.uuid)},
            key='account_created'
        )
        return self.save(instance=account)

    def update(self, uuid, **kwargs):
        accounts = self.find(uuid=uuid)
        if not accounts.total:
            self.error(code=HTTPStatus.NOT_FOUND)
        return self.apply(instance=accounts.items[0], **kwargs)

    def apply(self, instance, **kwargs):
        account = self.assign_attr(instance=instance, attr=kwargs)
        _ = self.notify(
            topic='accounts',
            value={'uuid': str(account.uuid)},
            key='account_updated'
        )
        return self.save(instance=account)

    def destroy(self, uuid, ):
        accounts = self.find(uuid=uuid)
        if not accounts.total:
            self.error(code=HTTPStatus.NOT_FOUND)
        return Base.destroy(self, instance=accounts.items[0])

    def handle_event(self, key, data):
        if key == 'auth_created':
            # create an account
            _ = Account().create(membership_uuid=data['uuid'], username=data['username'], email=data['email'],
                                 status='active', role='member')

    def generate_mail(self, uuid, type):
        accounts = self.find(uuid=uuid)
        if not accounts.total:
            self.error(code=HTTPStatus.NOT_FOUND)
        account = accounts.items[0]

        # handle various types of mail here
        if type == 'register':
            subject = 'Tech Tapir Registration'
            body = self.mail.generate_body('register', user=account)

        return {
            'to': account.email,
            'subject': subject,
            'html': body
        }
