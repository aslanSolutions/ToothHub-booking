from marshmallow import Schema, fields

class WishlistSchema(Schema):
    patient_id = fields.Str(required=True)
    date = fields.Date(required=True)
