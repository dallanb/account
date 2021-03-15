import logging
from http import HTTPStatus
from sqlalchemy_utils import PhoneNumber
from .base import Base
from ..models import Phone as PhoneModel


class Phone(Base):
    def __init__(self):
        Base.__init__(self)
        self.logger = logging.getLogger(__name__)
        self.phone_model = PhoneModel

    def find(self, **kwargs):
        return self._find(model=self.phone_model, **kwargs)

    def create(self, **kwargs):
        phone = self._init(model=self.phone_model, **kwargs)
        return self._save(instance=phone)

    def update(self, uuid, **kwargs):
        phones = self.find(uuid=uuid)
        if not phones.total:
            self.error(code=HTTPStatus.NOT_FOUND)
        return self.apply(instance=phones.items[0], **kwargs)

    def apply(self, instance, **kwargs):
        phone = self._assign_attr(instance=instance, attr=kwargs)
        return self._save(instance=phone)

    def destroy(self, uuid):
        phones = self.find(uuid=uuid)
        if not phones.total:
            self.error(code=HTTPStatus.NOT_FOUND)
        return self._destroy(instance=phones.items[0])

    @staticmethod
    def format(attr):
        return {
            'number': PhoneNumber(
                attr['_number'],
                attr['country_code']
            ),
            'extension': attr['extension']
        }
