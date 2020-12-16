from flask import request
from flask_restful import marshal_with

from .schema import *
from ..base import Base
from ....common.auth import assign_user
from ....common.response import DataResponse
from ....services import AvatarService, AccountService


class AvatarsAPI(Base):
    def __init__(self):
        Base.__init__(self)
        self.avatar = AvatarService()
        self.account = AccountService()

    @marshal_with(DataResponse.marshallable())
    @assign_user
    def post(self, uuid):
        data = self.clean(schema=create_schema, instance=request.form)

        accounts = self.account.find(uuid=uuid, include=['avatar'])
        if not accounts.total:
            self.throw_error(http_code=self.code.NOT_FOUND)

        account = accounts.items[0]
        s3_filename = self.avatar.generate_s3_filename(membership_uuid=str(account.membership_uuid))

        avatar = account.avatar
        _ = self.avatar.upload_fileobj(file=data['avatar'], filename=s3_filename)
        if not avatar:
            avatar = self.avatar.create(s3_filename=s3_filename)
            self.account.apply(instance=accounts.items[0], avatar=avatar)
        return DataResponse(
            data={
                'avatars': self.dump(
                    schema=dump_schema,
                    instance=avatar
                )
            }
        )
