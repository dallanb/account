import logging
from .base import Base
from ..models import Membership as MembershipModel
from .account import Account


class Membership(Base):
    def __init__(self):
        Base.__init__(self)
        self.logger = logging.getLogger(__name__)
        self.membership_model = MembershipModel

    def find(self, **kwargs):
        return Base.find(self, model=self.membership_model, **kwargs)

    def create(self, **kwargs):
        membership = self.init(model=self.membership_model, **kwargs)
        return self.save(instance=membership)

    def handle_event(self, key, data):
        if key == 'auth_created':
            # create an account
            membership_uuid = data['uuid']
            account = Account().create(status='active', role='basic')
            _ = self.create(membership_uuid=membership_uuid, account=account)
