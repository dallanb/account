from marshmallow import validate, Schema, post_dump
from webargs import fields


class DumpMailSchema(Schema):
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


class FetchMailSchema(Schema):
    type = fields.String()


dump_schema = DumpMailSchema()
dump_many_schema = DumpMailSchema(many=True)
fetch_schema = FetchMailSchema()
