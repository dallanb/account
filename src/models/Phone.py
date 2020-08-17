from sqlalchemy_utils import PhoneNumber
from .. import db
from .mixins import BaseMixin


class Phone(db.Model, BaseMixin):
    _number = db.Column(db.Unicode(20), nullable=False)
    country_code = db.Column(db.Unicode(8), nullable=False)
    extension = db.Column(db.Unicode(20), nullable=True)

    number = db.orm.composite(
        PhoneNumber,
        _number,
        country_code
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


Phone.register()
