import logging
from marshmallow import validate, Schema, post_dump
from webargs import fields
from ..addresses.schema import DumpAddressSchema, UpdateAddressSchema
from ..phones.schema import DumpPhoneSchema, UpdatePhoneSchema


class DumpAccountSchema(Schema):
    uuid = fields.UUID()
    ctime = fields.Integer()
    mtime = fields.Integer()
    first_name = fields.String()
    last_name = fields.String()
    address = fields.Nested(DumpAddressSchema)
    phone = fields.Nested(DumpPhoneSchema)

    def get_attribute(self, obj, attr, default):
        if attr == 'address':
            return getattr(obj, attr, default) if any(
                attr in include for include in self.context.get('include', [])) else None
        if attr == 'phone':
            return getattr(obj, attr, default) if any(
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
    first_name = fields.Str(required=False, missing=None)
    last_name = fields.Str(required=False, missing=None)
    address = fields.Nested(UpdateAddressSchema, missing=None, attribute='address', data_key='address')
    phone = fields.Nested(UpdatePhoneSchema, missing=None, attribute='phone', data_key='phone')


class FetchAllAccountSchema(Schema):
    page = fields.Int(required=False, missing=1)
    per_page = fields.Int(required=False, missing=10)
    include = fields.DelimitedList(fields.String(), required=False, missing=[])
    first_name = fields.String(required=False)
    last_name = fields.String(required=False)


dump_schema = DumpAccountSchema()
dump_many_schema = DumpAccountSchema(many=True)
update_schema = UpdateAccountSchema()
fetch_all_schema = FetchAllAccountSchema()
