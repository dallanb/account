from .schema import DisplayNameUpdatedSchema
from ..base import Base


class display_name_updated(Base):
    key = 'display_name_updated'
    schema = DisplayNameUpdatedSchema()

    def __init__(self, data):
        super().__init__(key=self.key, data=data)

    @classmethod
    def from_data(cls, account):
        data = cls.schema.dump({'account': account})
        return display_name_updated(data=data)
