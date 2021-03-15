from marshmallow import Schema
from webargs import fields


class AccountActiveSchema(Schema):
    uuid = fields.UUID(missing=None, attribute='account.uuid')
