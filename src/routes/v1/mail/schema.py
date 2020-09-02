from marshmallow import Schema
from webargs import fields


class FetchMailSchema(Schema):
    type = fields.String()


fetch_schema = FetchMailSchema()
