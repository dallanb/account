from sqlalchemy_utils import URLType
from .. import db
from .mixins import BaseMixin


class Avatar(db.Model, BaseMixin):
    s3_url = db.Column(URLType, nullable=False)
    filename = db.Column(db.String, nullable=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


Avatar.register()
