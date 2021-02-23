import logging
from http import HTTPStatus

from .base import Base
from ..decorators import account_notification
from ..models import Account as AccountModel


class Account(Base):
    def __init__(self):
        Base.__init__(self)
        self.logger = logging.getLogger(__name__)
        self.account_model = AccountModel

    def find(self, **kwargs):
        return self._find(model=self.account_model, **kwargs)

    @account_notification(operation='create')
    def create(self, **kwargs):
        account = self._init(model=self.account_model, **kwargs)
        return self._save(instance=account)

    def update(self, uuid, **kwargs):
        accounts = self.find(uuid=uuid)
        if not accounts.total:
            self.error(code=HTTPStatus.NOT_FOUND)
        return self.apply(instance=accounts.items[0], **kwargs)

    @account_notification(operation='update')
    def apply(self, instance, **kwargs):
        account = self._assign_attr(instance=instance, attr=kwargs)
        return self._save(instance=account)

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
