from .. import db
from .mixins import BaseMixin


class Avatar(db.Model, BaseMixin):
    s3_filename = db.Column(db.String, nullable=False)
    filename = db.Column(db.String, nullable=False)

    # Relationship
    account = db.relationship("Account", back_populates="avatar", uselist=False, lazy="noload")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


Avatar.register()
