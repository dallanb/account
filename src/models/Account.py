from sqlalchemy_utils import UUIDType
from .. import db
from .mixins import BaseMixin
from ..common import RoleEnum, StatusEnum


class Account(db.Model, BaseMixin):
    owner_uuid = db.Column(UUIDType(binary=False), nullable=False)

    # FK
    status = db.Column(db.Enum(StatusEnum), db.ForeignKey('status.name'), nullable=False)
    role = db.Column(db.Enum(RoleEnum), db.ForeignKey('role.name'), nullable=False)
    address_uuid = db.Column(UUIDType(binary=False), db.ForeignKey('address.uuid'), nullable=False)
    phone_uuid = db.Column(UUIDType(binary=False), db.ForeignKey('phone.uuid'), nullable=False)
    membership_uuid = db.Column(UUIDType(binary=False), db.ForeignKey('membership.uuid'), nullable=False)

    # Relationship
    account_status = db.relationship("Status")
    account_role = db.relationship("Role")
    account_address = db.relationship("Address")
    account_phone = db.relationship("Phone")
    account_membership = db.relationship("Membership")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


Account.register()
