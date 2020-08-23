import logging
from .base import Base
from ..models import Account as AccountModel
from http import HTTPStatus


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
