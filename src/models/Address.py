from sqlalchemy_utils import CountryType
from .. import db
from .mixins import BaseMixin


class Address(db.Model, BaseMixin):
    line_1 = db.Column(db.String, nullable=True)
    line_2 = db.Column(db.String, nullable=True)
    city = db.Column(db.String, nullable=True)
    province = db.Column(db.String, nullable=True)
    country = db.Column(CountryType, nullable=False)
    postal_code = db.Column(db.String, nullable=True)

    # Relationship
    account = db.relationship("Account", back_populates="address", uselist=False, lazy="noload")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


Address.register()
