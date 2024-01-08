from marshmallow import Schema, fields

class BookingSchema(Schema):
    _id = _id = fields.String(attribute='_id', dump_only=True)
    patient_email = fields.Email(required=True)
    dentist_email = fields.Email(required=True)
    clinic = fields.Str(required=True)
    appointment_datetime = fields.DateTime(required=True)
