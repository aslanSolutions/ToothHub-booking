from marshmallow import Schema, fields

class TimeSlotSchema(Schema):
    start_time = fields.DateTime(required=True)
    end_time = fields.DateTime(required=True)
    booked = fields.Boolean(missing=False)

class AvailabilityTimeSchema(Schema):
    dentist_email = fields.Str(required=True)
    date = fields.Date(required=True)
    time_slots = fields.List(fields.Nested(TimeSlotSchema), required=True)
