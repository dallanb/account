from .schema import AccountInactiveSchema
from ..base import Base


class account_inactive(Base):
    key = 'account_inactive'
    schema = AccountInactiveSchema()

    def __init__(self, data):
        super().__init__(key=self.key, data=data)

    @classmethod
    def from_data(cls, account):
        data = cls.schema.dump({'account': account})
        return account_inactive(data=data)
