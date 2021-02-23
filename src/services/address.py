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
        return self._find(model=self.address_model, **kwargs)

    def create(self, **kwargs):
        address = self._init(model=self.address_model, **kwargs)
        return self._save(instance=address)

    def update(self, uuid, **kwargs):
        addresses = self.find(uuid=uuid)
        if not addresses.total:
            self.error(code=HTTPStatus.NOT_FOUND)
        return self.apply(instance=addresses.items[0], **kwargs)

    def apply(self, instance, **kwargs):
        address = self._assign_attr(instance=instance, attr=kwargs)
        return self._save(instance=address)

    def destroy(self, uuid, ):
        addresses = self.find(uuid=uuid)
        if not addresses.total:
            self.error(code=HTTPStatus.NOT_FOUND)
        return self._destroy(instance=addresses.items[0])
