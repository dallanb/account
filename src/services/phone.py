import logging
from .base import Base
from ..models import Phone as PhoneModel
from http import HTTPStatus


class Phone(Base):
    def __init__(self):
        Base.__init__(self)
        self.logger = logging.getLogger(__name__)
        self.phone_model = PhoneModel

    def find(self, **kwargs):
        return Base.find(self, model=self.phone_model, **kwargs)

    def create(self, **kwargs):
        phone = self.init(model=self.phone_model, **kwargs)
        return self.save(instance=phone)

    def update(self, uuid, **kwargs):
        phones = self.find(uuid=uuid)
        if not phones.total:
            self.error(code=HTTPStatus.NOT_FOUND)
        return self.apply(instance=phones.items[0], **kwargs)

    def apply(self, instance, **kwargs):
        phone = self.assign_attr(instance=instance, attr=kwargs)
        return self.save(instance=phone)

    def destroy(self, uuid, ):
        phones = self.find(uuid=uuid)
        if not phones.total:
            self.error(code=HTTPStatus.NOT_FOUND)
        return Base.destroy(self, instance=phones.items[0])
