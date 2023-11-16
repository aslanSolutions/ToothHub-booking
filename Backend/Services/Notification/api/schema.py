from marshmallow import Schema, fields

class NotificationSchema(Schema):
    title = fields.Str(required=True)
    description = fields.Str(required=True)
    date = fields.Date(required=True)
    time = fields.Time(required=True)