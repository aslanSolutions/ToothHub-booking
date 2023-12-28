from datetime import datetime
import json
from flask import Blueprint, jsonify, request
from marshmallow import ValidationError
from .schema import BookingSchema
from .db import times
from .broker_routes import publishMessage, wait_for_acknowledgment
import requests
import uuid
from bson import ObjectId

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
        # validate_url = "http://127.0.0.1:5005/auth/validate"
        # headers = {"Authorization": request.headers.get('Authorization')}
        # validate_response = requests.get(validate_url, headers=headers)

        if True:
            correlation_id = str(uuid.uuid4())
            appointment_data['correlation_id'] = correlation_id
            message_json = json.dumps(appointment_data, default=lambda x: x.isoformat(
            ) if isinstance(x, datetime) else None)
            publish_result = publishMessage("booking/create", message_json)
            if publish_result is not None:
                return {'error': publish_result}, 501

            confirmation = wait_for_acknowledgment(correlation_id)
            if confirmation == True:
                del appointment_data['correlation_id']
                result = times.insert_one(appointment_data)
                new_appointment_id = result.inserted_id
                created_appointment = times.find_one(
                    {'_id': new_appointment_id})
                created_appointment['_id'] = str(created_appointment['_id'])

                # Publish confirmation of successful booking
                confirmation_message = {
                    "status": "success",
                    "dentist_email": appointment_data['dentist_email'],
                    "appointment_datetime": appointment_data['appointment_datetime'].isoformat(),
                }
                confirmation_result = publishMessage("booking/confirm",
                               json.dumps(confirmation_message))
                if confirmation_result is not None:
                    return {'error': publish_result}, 501

                return jsonify(created_appointment), 201

            else:
                return jsonify({"message": "The chosen date is not available anymore"}), 404
        else:
            # Validation failed
            return jsonify({"message": "User validation failed"}), validate_response.status_code

    except ValidationError as err:
        return jsonify(err.messages), 400


@bp.route('/<string:appointment_id>', methods=['DELETE'])
def delete_appointment_endpoint(appointment_id):
    try:
        correlation_id = str(uuid.uuid4())
        object_id = ObjectId(appointment_id)
        appointment_data = times.find_one({"_id": object_id})

        if appointment_data:
            appointment_data['_id'] = str(appointment_data['_id'])
            appointment_data['correlation_id'] = correlation_id

            message_json = json.dumps(appointment_data, default=str)

            publish_result = publishMessage("booking/delete", message_json)
            if publish_result is not None:
                return {'error': publish_result}, 501

            confirmation = wait_for_acknowledgment(correlation_id)
            if confirmation == True:
                result = times.delete_one({'_id': object_id})
                if result.deleted_count > 0:
                    return jsonify({"message": "Appointment deleted successfully"}), 200
                else:
                    return {"message": "Appointment not found"}, 404
            else:
                return {"message": "Could not delete the appointment, please try again later"}, 501
        else:
            return {"message": "Appointment not found"}, 404

    except Exception as e:
        return jsonify({'error': str(e)}), 501
@bp.route('/<string:appointment_id>', methods=['GET'])
def get_appointment_endpoint(appointment_id):
    """
    Endpoint to get a single appointment.
    Expects an appointment ID.
    Returns the appointment details and status code 200 if found.
    """
    try:
        schema = BookingSchema()
        object_id = ObjectId(appointment_id)
        appointment = times.find_one({'_id': object_id})
        if appointment:
            return jsonify(schema.dump(appointment)), 200
        else:
            return {"message": "Appointment not found"}, 404
    except Exception as e:
        return jsonify({'error': str(e)}), 501


@bp.route('/', methods=['GET'])
def get_all_appointments_endpoint():
    """
    Endpoint to get all appointments.
    Returns a list of appointments and status code 200.
    """
    appointments = list(times.find())
    schema = BookingSchema(many=True)
    return jsonify(schema.dump(appointments)), 200


@bp.route('/<string:appointment_id>', methods=['PATCH'])
def update_appointment_endpoint(appointment_id):
    """
    Endpoint to update an appointment.
    Expects an appointment ID and a JSON payload with updated details.
    Returns a success message and status code 200 if successful.
    """
    schema = BookingSchema()
    try:
        object_id = ObjectId(appointment_id)
        appointment_data = schema.load(request.json)
        correlation_id = str(uuid.uuid4())
        appointment_data['correlation_id'] = correlation_id
        appointment_data['id'] = str(object_id)
        message_json = json.dumps(appointment_data, default=lambda x: x.isoformat(
        ) if isinstance(x, datetime) else None)
        publish_result = publishMessage("booking/update", message_json)
        if publish_result is not None:
            return {'error': publish_result}, 501

        confirmation = wait_for_acknowledgment(correlation_id)
        if confirmation == True:
            result = times.update_one(
                {'_id': object_id}, {'$set': appointment_data})
            if result.matched_count:
                return jsonify(schema.dump(appointment_data)), 200
            else:
                return jsonify({"message": "Appointment not found"}), 404
        else:
            return jsonify({"message": "Appointment Could not be updated plase try againe later"}), 404
    except ValidationError as err:
        return jsonify(err.messages), 400
