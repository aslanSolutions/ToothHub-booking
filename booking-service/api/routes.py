from flask import Blueprint, jsonify, request
from marshmallow import ValidationError
from .schema import BookingSchema
from .db import times

bp = Blueprint('appointments', __name__, url_prefix='/appointments')

@bp.route('/appointment', methods=['POST'])
def create_appointment_endpoint():
    """
    Endpoint to create an appointment.
    Expects a JSON payload with appointment details.
    Returns a success message and status code 201 if successful.
    """
    schema = BookingSchema()
    try:
        appointment_data = schema.load(request.json)
        times.insert_one(appointment_data)
        return jsonify({"message": "Appointment created successfully"}), 201
    except ValidationError as err:
        return jsonify(err.messages), 400

@bp.route('/appointments/<string:appointment_id>', methods=['DELETE'])
def delete_appointment_endpoint(appointment_id):
    """
    Endpoint to delete an appointment.
    Expects an appointment ID.
    Returns a success message and status code 200 if successful.
    """
    result = times.delete_one({'_id': appointment_id})
    if result.deleted_count:
        return jsonify({"message": "Appointment deleted successfully"}), 200
    else:
        return jsonify({"message": "Appointment not found"}), 404

@bp.route('/appointments/<string:appointment_id>', methods=['GET'])
def get_appointment_endpoint(appointment_id):
    """
    Endpoint to get a single appointment.
    Expects an appointment ID.
    Returns the appointment details and status code 200 if found.
    """
    appointment = times.find_one({'_id': appointment_id})
    if appointment:
        schema = BookingSchema()
        return jsonify(schema.dump(appointment)), 200
    else:
        return jsonify({"message": "Appointment not found"}), 404

@bp.route('/appointments', methods=['GET'])
def get_all_appointments_endpoint():
    """
    Endpoint to get all appointments.
    Returns a list of appointments and status code 200.
    """
    appointments = list(times.find())
    schema = BookingSchema(many=True)
    return jsonify(schema.dump(appointments)), 200

@bp.route('/appointment/<string:appointment_id>', methods=['PATCH'])
def update_appointment_endpoint(appointment_id):
    """
    Endpoint to update an appointment.
    Expects an appointment ID and a JSON payload with updated details.
    Returns a success message and status code 200 if successful.
    """
    schema = BookingSchema()
    try:
        appointment_data = schema.load(request.json)
        result = times.update_one({'_id': appointment_id}, {'$set': appointment_data})
        if result.matched_count:
            return jsonify({"message": "Appointment updated successfully"}), 200
        else:
            return jsonify({"message": "Appointment not found"}), 404
    except ValidationError as err:
        return jsonify(err.messages), 400
