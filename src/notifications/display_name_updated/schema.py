from marshmallow import Schema
from webargs import fields


class DisplayNameUpdatedSchema(Schema):
    uuid = fields.UUID(attribute='account.uuid')
    user_uuid = fields.UUID(attribute='account.user_uuid')
    display_name = fields.String(attribute='account.display_name')
