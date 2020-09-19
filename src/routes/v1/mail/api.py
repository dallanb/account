from flask import request
from flask_restful import marshal_with

from .schema import *
from ..base import Base
from ....common.response import DataResponse
from ....common.auth import check_user, assign_user
from ....services import Account


class MailAPI(Base):
    def __init__(self):
        Base.__init__(self)
        self.account = Account()

    @marshal_with(DataResponse.marshallable())
    @check_user
    @assign_user
    def get(self, uuid):
        data = self.clean(schema=fetch_schema, instance=request.args)
        mail = self.account.generate_mail(uuid=uuid, type=data['type'])
        return DataResponse(
            data={
                'mail': mail
            }
        )
