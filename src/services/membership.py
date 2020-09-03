import logging
from .base import Base
from ..models import Membership as MembershipModel
from .account import Account
from http import HTTPStatus


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
            account = Account().create(status='active', role='member')
            _ = self.create(membership_uuid=data['uuid'], username=data['username'], email=data['email'],
                            account=account)

    def generate_mail(self, uuid, type):
        memberships = self.find(account_uuid=uuid)
        if not memberships.total:
            self.error(code=HTTPStatus.NOT_FOUND)
        membership = memberships.items[0]

        # handle various types of mail here
        if type == 'register':
            subject = 'Tech Tapir Registration'
            body = self.mail.generate_body('register', user=membership)

        return {
            'to': membership.email,
            'subject': subject,
            'html': body
        }
