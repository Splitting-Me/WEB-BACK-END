from marshmallow import Schema, EXCLUDE, fields
from lib import ObjectIdField
class ResponseUserSchmas(Schema):
    class Meta:
        unknown=EXCLUDE
        ordered=True
    total = fields.Int()
    rank = fields.Int()

class ReferralSchema(Schema):
    class Meta:
        unknown =EXCLUDE
        ordered=True
    user_address = fields.String(required=True)
    referral_address = fields.String()
    signature = fields.String(default='', missing='')
    nonce = fields.Int()

class IpfsSchema(Schema):
    class Meta:
        unknown =EXCLUDE
        ordered=True
    image = fields.String()
    name = fields.String()
    description = fields.String()

class IpfsResponseSchema(Schema):
    class Meta:
        unknown =EXCLUDE
        ordered=True
    url = fields.String()