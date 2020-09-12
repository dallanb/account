from flask import request
from flask_restful import marshal_with

from .schema import *
from ..base import Base
from ....common.auth import check_user, assign_user
from ....common.response import DataResponse
from ....services import Account, Address, Phone


class AccountsAPI(Base):
    def __init__(self):
        Base.__init__(self)
        self.account = Account()
        self.address = Address()
        self.phone = Phone()

    @marshal_with(DataResponse.marshallable())
    @check_user
    @assign_user
    def get(self, uuid):
        data = self.clean(schema=fetch_schema, instance=request.args)
        accounts = self.account.find(uuid=uuid, **data)
        if not accounts.total:
            self.throw_error(http_code=self.code.NOT_FOUND)
        return DataResponse(
            data={
                'accounts': self.dump(
                    schema=dump_schema,
                    instance=accounts.items[0],
                    params={
                        'include': data['include'],
                        'expand': data['expand']
                    }
                )
            }
        )

    @marshal_with(DataResponse.marshallable())
    @check_user
    @assign_user
    def put(self, uuid=None):
        data = self.clean(schema=update_schema, instance=request.get_json())
        accounts = self.account.find(uuid=uuid)
        if not accounts.total:
            self.throw_error(http_code=self.code.NOT_FOUND)

        account = accounts.items[0]

        address_attr = data.pop('address')
        if address_attr:
            if account.address:
                account.address = self.address.apply(instance=account.address, **address_attr)
            else:
                account.address = self.address.create(**address_attr)

        phone_attr = data.pop('phone')
        if phone_attr:
            phone = self.phone.format(attr=phone_attr)
            if account.phone:
                account.phone = self.phone.apply(instance=account.phone, **phone)
            else:
                account.phone = self.phone.create(**phone)

        account = self.account.apply(instance=account, **data)
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
    @check_user
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


class AccountsListSearchAPI(Base):
    def __init__(self):
        Base.__init__(self)
        self.account = Account()

    @marshal_with(DataResponse.marshallable())
    @check_user
    def get(self):
        data = self.clean(schema=search_schema, instance=request.args)
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
                    instance=accounts.items
                )
            }
        )
