from marshmallow import Schema, post_dump
from webargs import fields


class DumpAddressSchema(Schema):
    uuid = fields.UUID()
    ctime = fields.Integer()
    mtime = fields.Integer()
    line_1 = fields.String()
    line_2 = fields.String()
    city = fields.String()
    province = fields.String()
    country = fields.String()
    postal_code = fields.String()

    def get_attribute(self, obj, attr, default):
        if attr == 'country':
            return getattr(obj.country, 'code', default)
        return getattr(obj, attr, default)

    @post_dump
    def make_obj(self, data, **kwargs):
        return data


class UpdateAddressSchema(Schema):
    line_1 = fields.Str(required=False, missing=None)
    line_2 = fields.Str(required=False, missing=None)
    city = fields.Str(required=False, missing=None)
    province = fields.Str(required=False, missing=None)
    country = fields.Str(required=False, missing=None)
    postal_code = fields.Str(required=False, missing=None)


dump_schema = DumpAddressSchema()
dump_many_schema = DumpAddressSchema(many=True)
update_schema = UpdateAddressSchema()
