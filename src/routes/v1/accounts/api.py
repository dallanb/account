from flask import request
from flask_restful import marshal_with

from .schema import *
from ..base import Base
from ....common.auth import assign_user
from ....common.response import DataResponse
from ....services import AccountService, AddressService, PhoneService


class AccountsAPI(Base):
    def __init__(self):
        Base.__init__(self)
        self.account = AccountService()
        self.address = AddressService()
        self.phone = PhoneService()

    @marshal_with(DataResponse.marshallable())
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
    @assign_user
    def put(self, uuid=None):
        data = self.clean(schema=update_schema, instance=request.get_json())
        accounts = self.account.find(uuid=uuid)
        if not accounts.total:
            self.throw_error(http_code=self.code.NOT_FOUND)

        account = accounts.items[0]

        address_attr = data.pop('address', None)
        if address_attr:
            if account.address:
                account.address = self.address.apply(instance=account.address, **address_attr)
            else:
                account.address = self.address.create(**address_attr)

        phone_attr = data.pop('phone', None)
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
        self.account = AccountService()

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


class AccountsListBulkAPI(Base):
    def __init__(self):
        Base.__init__(self)
        self.account = AccountService()

    @marshal_with(DataResponse.marshallable())
    def post(self):
        data = self.clean(schema=bulk_schema, instance={**request.get_json(), **request.args.to_dict()})
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


class AccountsMembershipAPI(Base):
    def __init__(self):
        Base.__init__(self)
        self.account = AccountService()

    @marshal_with(DataResponse.marshallable())
    def get(self, uuid):
        data = self.clean(schema=fetch_schema, instance=request.args)
        accounts = self.account.find(user_uuid=uuid, **data)
        if not accounts.total:
            self.throw_error(http_code=self.code.NOT_FOUND)
        return DataResponse(
            data={
                'membership': self.dump(
                    schema=dump_schema,
                    instance=accounts.items[0],
                    params={
                        'include': data['include'],
                        'expand': data['expand']
                    }
                )
            }
        )
