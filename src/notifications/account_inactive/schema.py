from marshmallow import Schema
from webargs import fields


class AccountInactiveSchema(Schema):
    uuid = fields.UUID(missing=None, attribute='account.uuid')
