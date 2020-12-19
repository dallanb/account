from sqlalchemy_utils import EmailType, UUIDType
from sqlalchemy_utils.types import TSVectorType

from .mixins import BaseMixin
from .. import db
from ..common import RoleEnum, StatusEnum


class Account(db.Model, BaseMixin):
    membership_uuid = db.Column(UUIDType(binary=False), primary_key=True, nullable=False)
    email = db.Column(EmailType, unique=True, nullable=False)
    username = db.Column(db.String(15), unique=True, nullable=False)
    display_name = db.Column(db.String(50), nullable=True)

    # Search
    search_vector = db.Column(TSVectorType('display_name', 'username', weights={'display_name': 'A', 'username': 'B'}))

    # FK
    status = db.Column(db.Enum(StatusEnum), db.ForeignKey('status.name'), nullable=False)
    role = db.Column(db.Enum(RoleEnum), db.ForeignKey('role.name'), nullable=False)
    address_uuid = db.Column(UUIDType(binary=False), db.ForeignKey('address.uuid'), nullable=True)
    phone_uuid = db.Column(UUIDType(binary=False), db.ForeignKey('phone.uuid'), nullable=True)
    avatar_uuid = db.Column(UUIDType(binary=False), db.ForeignKey('avatar.uuid'), nullable=True)

    # Relationship
    account_status = db.relationship("Status")
    account_role = db.relationship("Role")
    address = db.relationship("Address", back_populates="account")
    phone = db.relationship("Phone", back_populates="account")
    avatar = db.relationship("Avatar", back_populates="account")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


Account.register()
