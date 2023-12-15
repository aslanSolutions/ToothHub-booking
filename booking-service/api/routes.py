from flask import Blueprint, jsonify, request
from marshmallow import ValidationError
from .schema import BookingSchema
from .db import times
from .broker_routes import publishMessage
import requests

bp = Blueprint('appointments', __name__, url_prefix='/appointments')

@bp.route('/', methods=['POST'])
def create_appointment_endpoint():
    """
    Endpoint to create an appointment.
    Expects a JSON payload with appointment details.
    Returns a success message and status code 201 if successful.
    """
    schema = BookingSchema()

    appointment_data = schema.load(request.json)
    try:
        #validate_url = "http://127.0.0.1:5005/auth/validate"
        #headers = {"Authorization": request.headers.get('Authorization')}
        #validate_response = requests.get(validate_url, headers=headers)

        #if validate_response.status_code == 200:
        if True:
            result = times.insert_one(appointment_data)
            new_appointment_id = result.inserted_id
            created_appointment = times.find_one({'_id': new_appointment_id})


            date_str = appointment_data['appointment_datetime'].date().strftime('%Y-%m-%d')
            time_str = appointment_data['appointment_datetime'].time().strftime('%H:%M')
            message = f"A new appointment has been scheduled for you on {date_str} at {time_str}. Appointment id: {str(created_appointment['_id'])}"
            notification = {
                'subject': "New Appointment Scheduled",
                'description':message,
                'receiver':[appointment_data['dentist_email'], appointment_data['patient_email']]
            }


            publish_result = publishMessage("booking", 'created_appointment')
            print(publish_result)
            if publish_result is not None:
                return {'error': publish_result}, 501

            created_appointment['_id'] = str(created_appointment['_id'])
            return jsonify(created_appointment), 201
        else:
            # Validation failed
            return jsonify({"message": "User validation failed"}), validate_response.status_code
        
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

@bp.route('/all_appointments', methods=['GET'])
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
