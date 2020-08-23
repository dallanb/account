from sqlalchemy_utils import EmailType, PasswordType, UUIDType

from .. import db
from .mixins import BaseMixin


class Membership(db.Model, BaseMixin):
    membership_uuid = db.Column(UUIDType(binary=False), nullable=False)
    email = db.Column(EmailType, unique=True, nullable=False)
    username = db.Column(db.String(255), unique=True, nullable=False)

    # FK
    account_uuid = db.Column(UUIDType(binary=False), db.ForeignKey('account.uuid'), nullable=False)

    # Relationship
    account = db.relationship("Account")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


Membership.register()
