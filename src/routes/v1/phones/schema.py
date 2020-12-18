from marshmallow import validate, Schema, post_dump
from webargs import fields


class DumpPhoneSchema(Schema):
    uuid = fields.UUID()
    ctime = fields.Integer()
    mtime = fields.Integer()
    number = fields.String()
    country_code = fields.String()
    extension = fields.String()

    def get_attribute(self, obj, attr, default):
        return getattr(obj, attr, default)

    @post_dump
    def make_obj(self, data, **kwargs):
        return data


class UpdatePhoneSchema(Schema):
    number = fields.Str(required=True, attribute='_number')
    country_code = fields.Str(required=True)
    extension = fields.Str(required=False, missing=None)


dump_schema = DumpPhoneSchema()
dump_many_schema = DumpPhoneSchema(many=True)
update_schema = UpdatePhoneSchema()
