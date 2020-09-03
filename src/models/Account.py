from sqlalchemy_utils import UUIDType
from .. import db
from .mixins import BaseMixin
from ..common import RoleEnum, StatusEnum


class Account(db.Model, BaseMixin):
    first_name = db.Column(db.String, nullable=True)
    last_name = db.Column(db.String, nullable=True)

    # FK
    status = db.Column(db.Enum(StatusEnum), db.ForeignKey('status.name'), nullable=False)
    role = db.Column(db.Enum(RoleEnum), db.ForeignKey('role.name'), nullable=False)
    address_uuid = db.Column(UUIDType(binary=False), db.ForeignKey('address.uuid'), nullable=True)
    phone_uuid = db.Column(UUIDType(binary=False), db.ForeignKey('phone.uuid'), nullable=True)
    avatar_uuid = db.Column(UUIDType(binary=False), db.ForeignKey('avatar.uuid'), nullable=True)

    # Relationship
    account_status = db.relationship("Status")
    account_role = db.relationship("Role")
    address = db.relationship("Address", backref=db.backref("account", uselist=False))
    phone = db.relationship("Phone", backref=db.backref("account", uselist=False))
    avatar = db.relationship("Avatar", backref=db.backref("avatar", uselist=False))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


Account.register()
