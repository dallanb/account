import logging
from .base import Base
from ..models import Address as AddressModel
from http import HTTPStatus


class Address(Base):
    def __init__(self):
        Base.__init__(self)
        self.logger = logging.getLogger(__name__)
        self.address_model = AddressModel

    def find(self, **kwargs):
        return Base.find(self, model=self.address_model, **kwargs)

    def create(self, **kwargs):
        address = self.init(model=self.address_model, **kwargs)
        return self.save(instance=address)

    def update(self, uuid, **kwargs):
        addresses = self.find(uuid=uuid)
        if not addresses.total:
            self.error(code=HTTPStatus.NOT_FOUND)
        return self.apply(instance=addresses.items[0], **kwargs)

    def apply(self, instance, **kwargs):
        address = self.assign_attr(instance=instance, attr=kwargs)
        return self.save(instance=address)

    def destroy(self, uuid, ):
        addresses = self.find(uuid=uuid)
        if not addresses.total:
            self.error(code=HTTPStatus.NOT_FOUND)
        return Base.destroy(self, instance=addresses.items[0])
