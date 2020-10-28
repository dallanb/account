from flask import request
from flask_restful import marshal_with

from .schema import *
from ..base import Base
from ....common.response import DataResponse
from ....common.auth import assign_user
from ....services import Avatar, Account


class AvatarsAPI(Base):
    def __init__(self):
        Base.__init__(self)
        self.avatar = Avatar()
        self.account = Account()

    @marshal_with(DataResponse.marshallable())
    @assign_user
    def post(self, uuid):
        data = self.clean(schema=create_schema, instance=request.files)

        accounts = self.account.find(uuid=uuid, include=['avatar'])
        if not accounts.total:
            self.throw_error(http_code=self.code.NOT_FOUND)

        account = accounts.items[0]
        s3_filename = self.avatar.generate_s3_filename(filename=data['filename'],
                                                       membership_uuid=str(account.membership_uuid))
        data['avatar'].filename = s3_filename

        avatar = account.avatar
        if avatar:
            # preserve original s3_filename but replace the filename to the filename of the new file
            _ = self.avatar.upload_fileobj(file=data['avatar'])
            avatar = self.avatar.apply(instance=avatar, filename=avatar.filename)
        else:
            _ = self.avatar.upload_fileobj(file=data['avatar'])
            avatar = self.avatar.create(filename=data['filename'], s3_filename=s3_filename)
            self.account.apply(instance=accounts.items[0], avatar=avatar)
        return DataResponse(
            data={
                'avatars': self.dump(
                    schema=dump_schema,
                    instance=avatar
                )
            }
        )
