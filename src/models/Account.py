from sqlalchemy_utils import UUIDType
from sqlalchemy.ext.hybrid import hybrid_property
from .. import db
from .mixins import BaseMixin
from ..common import RoleEnum, StatusEnum


class Account(db.Model, BaseMixin):
    first_name = db.Column(db.String, nullable=True)
    last_name = db.Column(db.String, nullable=True)
    # name = db.column_property(first_name + " " + last_name)

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

    @hybrid_property
    def name(self):
        return f'{self.first_name} {self.last_name}'

    @name.setter
    def name(self, value):
        self.first_name, self.last_name = value.split(' ', 1)

    @name.expression
    def name(self):
        return db.func.concat(self.first_name, ' ', self.last_name)


Account.register()
