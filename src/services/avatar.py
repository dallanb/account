import logging
from http import HTTPStatus
from .. import app
from .base import Base
from ..models import Avatar as AvatarModel
from ..libs import S3
from ..common.utils import s3_object_name


class Avatar(Base):
    def __init__(self):
        Base.__init__(self)
        self.logger = logging.getLogger(__name__)
        self.s3 = S3(aws_access_key_id=app.config['S3_ACCESS_KEY'], aws_secret_access_key=app.config['S3_SECRET_KEY'])
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
        result = self.s3.upload(filename=filename, bucket=app.config['S3_BUCKET'],
                                object_name=s3_object_name(filename))
        if not result:
            self.error(code=HTTPStatus.INTERNAL_SERVER_ERROR)
        return result

    def upload_fileobj(self, file):
        result = self.s3.upload_obj(
            file=file,
            bucket=app.config['S3_BUCKET'],
            object_name=s3_object_name(file.filename),
            extra_args={
                "ACL": "public-read",
                "ContentType": file.content_type
            }
        )
        if not result:
            self.error(code=HTTPStatus.INTERNAL_SERVER_ERROR)
        return
