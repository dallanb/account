from .schema import AccountActiveSchema
from ..base import Base


class account_active(Base):
    key = 'account_active'
    schema = AccountActiveSchema()

    def __init__(self, data):
        super().__init__(key=self.key, data=data)

    @classmethod
    def from_data(cls, account):
        data = cls.schema.dump({'account': account})
        return account_active(data=data)
