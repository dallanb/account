from marshmallow import Schema, post_dump, post_load
from marshmallow_enum import EnumField
from webargs import fields

from ..addresses.schema import DumpAddressSchema, UpdateAddressSchema
from ..phones.schema import DumpPhoneSchema, UpdatePhoneSchema
from ....common import StatusEnum


class DumpAccountSchema(Schema):
    uuid = fields.UUID()
    ctime = fields.Integer()
    mtime = fields.Integer()
    user_uuid = fields.UUID()
    email = fields.String()
    username = fields.String()
    display_name = fields.String()
    status = EnumField(StatusEnum)
    address = fields.Nested(DumpAddressSchema)
    phone = fields.Nested(DumpPhoneSchema)

    def get_attribute(self, obj, attr, default):
        if attr == 'address':
            return getattr(obj, attr, default) or {} if any(
                attr in include for include in self.context.get('include', [])) else None
        if attr == 'phone':
            return getattr(obj, attr, default) or {} if any(
                attr in include for include in self.context.get('include', [])) else None
        else:
            return getattr(obj, attr, default)

    @post_dump
    def make_obj(self, data, **kwargs):
        if data.get('address', False) is None:
            del data['address']
        if data.get('phone', False) is None:
            del data['phone']
        return data


class UpdateAccountSchema(Schema):
    display_name = fields.Str(required=False, missing=None)
    address = fields.Nested(UpdateAddressSchema, missing=None, attribute='address', data_key='address')
    phone = fields.Nested(UpdatePhoneSchema, missing=None, attribute='phone', data_key='phone')


class FetchAccountSchema(Schema):
    include = fields.DelimitedList(fields.String(), required=False, missing=[])
    expand = fields.DelimitedList(fields.String(), required=False, missing=[])


class FetchAllAccountSchema(Schema):
    page = fields.Int(required=False, missing=1)
    per_page = fields.Int(required=False, missing=10)
    include = fields.DelimitedList(fields.String(), required=False, missing=[])


class _BulkAccountWithinSchema(Schema):
    key = fields.String(required=True)
    value = fields.List(fields.String(), required=True)

    @post_load
    def clean_within(self, in_data, **kwargs):
        return {in_data['key']: in_data['value']}


class BulkAccountSchema(Schema):
    page = fields.Int(required=False, missing=1)
    per_page = fields.Int(required=False, missing=10)
    within = fields.Nested(_BulkAccountWithinSchema)
    include = fields.DelimitedList(fields.String(), required=False, missing=[])


dump_schema = DumpAccountSchema()
dump_many_schema = DumpAccountSchema(many=True)
update_schema = UpdateAccountSchema()
fetch_schema = FetchAccountSchema()
fetch_all_schema = FetchAllAccountSchema()
bulk_schema = BulkAccountSchema()
