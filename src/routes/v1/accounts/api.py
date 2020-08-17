from flask import request
from flask_restful import marshal_with
from .schema import *
from ..base import Base
from ....common.response import DataResponse
from ....common.auth import check_user
from ....services import Account, Address, Phone


class AccountsAPI(Base):
    def __init__(self):
        Base.__init__(self)
        self.account = Account()

    @marshal_with(DataResponse.marshallable())
    def get(self, uuid):
        accounts = self.account.find(uuid=uuid)
        if not accounts.total:
            self.throw_error(http_code=self.code.NOT_FOUND)
        return DataResponse(
            data={
                'accounts': self.dump(
                    schema=dump_schema,
                    instance=accounts.items[0]
                )
            }
        )

    @marshal_with(DataResponse.marshallable())
    @check_user
    def put(self, uuid):
        data = self.clean(schema=update_schema, instance=request.get_json())
        accounts = self.account.find(uuid=uuid)
        if not accounts.total:
            self.throw_error(http_code=self.code.NOT_FOUND)
            
        account = accounts.items[0]
        if data['address']:
            if account.address:
                account.address = self.address.apply(instance=account.address, **data['address'])
            else:
                account.address = self.address.create(**data['address'])
        if data['phone']:
            if account.phone:
                account.phone = self.phone.apply(instance=account.phone, **data['phone'])
            else:
                account.phone = self.phone.create(**data['phone'])
        account = self.account.apply(instance=account, **data['account'])
        return DataResponse(
            data={
                'accounts': self.dump(
                    schema=dump_schema,
                    instance=account
                )
            }
        )


class AccountsListAPI(Base):
    def __init__(self):
        Base.__init__(self)
        self.account = Account()

    @marshal_with(DataResponse.marshallable())
    def get(self):
        data = self.clean(schema=fetch_all_schema, instance=request.args)
        accounts = self.account.find(**data)
        return DataResponse(
            data={
                '_metadata': self.prepare_metadata(
                    total_count=accounts.total,
                    page_count=len(accounts.items),
                    page=data['page'],
                    per_page=data['per_page']),
                'accounts': self.dump(
                    schema=dump_many_schema,
                    instance=accounts.items,
                    params={
                        'include': data['include']
                    }
                )
            }
        )
