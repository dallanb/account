from .schema import AccountPendingSchema
from ..base import Base


class account_pending(Base):
    key = 'account_pending'
    schema = AccountPendingSchema()

    def __init__(self, data):
        super().__init__(key=self.key, data=data)

    @classmethod
    def from_data(cls, account):
        data = cls.schema.dump({'account': account})
        return account_pending(data=data)
