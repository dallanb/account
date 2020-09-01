import logging
from .. import app
from .base import Base
from ..models import Avatar as AvatarModel
from http import HTTPStatus


class Avatar(Base):
    def __init__(self):
        Base.__init__(self)
        self.logger = logging.getLogger(__name__)
        self.account_model = AvatarModel

    def find(self, **kwargs):
        return Base.find(self, model=self.account_model, **kwargs)

    def create(self, **kwargs):
        account = self.init(model=self.account_model, **kwargs)
        return self.save(instance=account)

    def update(self, uuid, **kwargs):
        avatars = self.find(uuid=uuid)
        if not avatars.total:
            self.error(code=HTTPStatus.NOT_FOUND)
        return self.apply(instance=avatars.items[0], **kwargs)

    def apply(self, instance, **kwargs):
        account = self.assign_attr(instance=instance, attr=kwargs)
        return self.save(instance=account)

    def destroy(self, uuid, ):
        avatars = self.find(uuid=uuid)
        if not avatars.total:
            self.error(code=HTTPStatus.NOT_FOUND)
        return Base.destroy(self, instance=avatars.items[0])

    def upload_file(self, filename):
        s3_client = boto3.client('s3')
        try:
            response = s3_client.upload_file(filename, app.config['S3_BUCKET'], filename)
