from marshmallow import Schema, post_dump
from webargs import fields

from ..addresses.schema import DumpAddressSchema, UpdateAddressSchema
from ..avatars.schema import DumpAvatarSchema
from ..phones.schema import DumpPhoneSchema, UpdatePhoneSchema


class DumpAccountSchema(Schema):
    uuid = fields.UUID()
    ctime = fields.Integer()
    mtime = fields.Integer()
    membership_uuid = fields.UUID()
    email = fields.String()
    username = fields.String()
    first_name = fields.String()
    last_name = fields.String()
    address = fields.Nested(DumpAddressSchema)
    phone = fields.Nested(DumpPhoneSchema)
    avatar = fields.Nested(DumpAvatarSchema)

    def get_attribute(self, obj, attr, default):
        if attr == 'address':
            return getattr(obj, attr, default) or {} if any(
                attr in include for include in self.context.get('include', [])) else None
        if attr == 'phone':
            return getattr(obj, attr, default) or {} if any(
                attr in include for include in self.context.get('include', [])) else None
        if attr == 'avatar':
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
        if data.get('avatar', False) is None:
            del data['avatar']
        return data


class UpdateAccountSchema(Schema):
    first_name = fields.Str(required=False, missing=None)
    last_name = fields.Str(required=False, missing=None)
    address = fields.Nested(UpdateAddressSchema, missing=None, attribute='address', data_key='address')
    phone = fields.Nested(UpdatePhoneSchema, missing=None, attribute='phone', data_key='phone')


class FetchAccountSchema(Schema):
    include = fields.DelimitedList(fields.String(), required=False, missing=[])
    expand = fields.DelimitedList(fields.String(), required=False, missing=[])


class FetchAllAccountSchema(Schema):
    page = fields.Int(required=False, missing=1)
    per_page = fields.Int(required=False, missing=10)
    include = fields.DelimitedList(fields.String(), required=False, missing=[])
    first_name = fields.String(required=False)
    last_name = fields.String(required=False)


class SearchAccountSchema(Schema):
    page = fields.Int(required=False, missing=1)
    per_page = fields.Int(required=False, missing=10)
    key = fields.String(attribute='search.key', data_key='key')
    fields = fields.DelimitedList(fields.String(), attribute='search.fields', data_key='fields')


class BulkAccountSchema(Schema):
    page = fields.Int(required=False, missing=1)
    per_page = fields.Int(required=False, missing=10)
    membership_uuid = fields.List(fields.String(), attribute='within.membership_uuid', data_key='membership_uuid')
    include = fields.DelimitedList(fields.String(), required=False, missing=[])


dump_schema = DumpAccountSchema()
dump_many_schema = DumpAccountSchema(many=True)
update_schema = UpdateAccountSchema()
fetch_schema = FetchAccountSchema()
fetch_all_schema = FetchAllAccountSchema()
search_schema = SearchAccountSchema()
bulk_schema = BulkAccountSchema()
