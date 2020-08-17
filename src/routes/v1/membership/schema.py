from marshmallow import fields, Schema


class DumpMembershipsSchema(Schema):
    uuid = fields.UUID()
    ctime = fields.Integer()
    mtime = fields.Integer()
    account = fields.Nested('DumpAccountSchema')
    membership_uuid = fields.UUID()


dump_schema = DumpMembershipsSchema()
dump_many_schema = DumpMembershipsSchema(many=True)
