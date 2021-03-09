from marshmallow import Schema, pre_dump
from webargs import fields


class CountryUpdatedSchema(Schema):
    uuid = fields.UUID(missing=None, attribute='account.uuid')
    country = fields.String()

    @pre_dump
    def prepare(self, data, **kwargs):
        data['account'] = data['address'].account
        data['country'] = data['address'].country.code
        return data
