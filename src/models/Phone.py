from sqlalchemy_utils import PhoneNumber

from .mixins import BaseMixin
from .. import db


class Phone(db.Model, BaseMixin):
    _number = db.Column(db.Unicode(20), nullable=False)
    country_code = db.Column(db.Unicode(8), nullable=False)
    extension = db.Column(db.Unicode(20), nullable=True)

    number = db.composite(
        PhoneNumber,
        _number,
        country_code
    )

    # Relationship
    account = db.relationship("Account", back_populates="phone", uselist=False, lazy="noload")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


Phone.register()
