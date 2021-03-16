from marshmallow import Schema
from webargs import fields


class AccountPendingSchema(Schema):
    uuid = fields.UUID(missing=None, attribute='account.uuid')
