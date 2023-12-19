from marshmallow import Schema, fields

class WishlistSchema(Schema):
    patient_email = fields.Str(required=True)
    date = fields.DateTime(required=True)
