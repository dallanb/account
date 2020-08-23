from ..common.enums import RoleEnum
from .. import db
from .mixins import EnumMixin


class Role(db.Model, EnumMixin):
    name = db.Column(db.Enum(RoleEnum), primary_key=True, unique=True, nullable=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


Role.register()
