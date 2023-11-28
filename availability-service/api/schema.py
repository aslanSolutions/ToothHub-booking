from marshmallow import Schema, fields

class TimeSlotSchema(Schema):
    time_slot_id = fields.Str(required=True)
    start_time = fields.DateTime(required=True)
    end_time = fields.DateTime(required=True)

class AvailabilityTimeSchema(Schema):
    dentist_email = fields.Str(required=True)
    date = fields.Date(required=True)
    time_slots = fields.List(fields.Nested(TimeSlotSchema), required=True)
