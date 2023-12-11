from flask import Blueprint, jsonify, request
from .schema import TimeSlotSchema, AvailabilityTimeSchema
from .db import times
from bson import json_util
import datetime

bp = Blueprint('availability', __name__, url_prefix='/availability')


@bp.route('/set_availability', methods=['POST'])
def set_availability():
    data = request.get_json()
    errors = AvailabilityTimeSchema().validate(data)
    if errors:
        return jsonify({"message": "Validation error", "errors": errors}), 400

    dentist_email = data.get('dentist_email')
    date = data.get('date')
    if not dentist_email or not date:
        return jsonify({"message": "Dentist email and date are required"}), 400

    # Check if an entry for this date and dentist already exists
    existing_entry = times.find_one(
        {'dentist_email': dentist_email, 'date': date})
    if existing_entry:
        new_time_slots = data.get('time_slots')
        times.update_one({'_id': existing_entry['_id']}, {
                         '$set': {'time_slots': new_time_slots}})
        updated_entry = times.find_one({'_id': existing_entry['_id']})
        return jsonify({"message": "Availability updated successfully", "availability": json_util.dumps(updated_entry)}), 200
    else:
        result = times.insert_one(data)
        new_availability_id = result.inserted_id
        created_availability = times.find_one({'_id': new_availability_id})
        return jsonify({"message": "Availability set successfully", "availability": json_util.dumps(created_availability)}), 201


@bp.route('/get_availability', methods=['GET'])
def get_availability():
    dentist_email = request.args.get('dentist_email')

    if not dentist_email:
        return jsonify({"message": "Dentist email is required"}), 400

    available_slots = times.find({'dentist_email': dentist_email}, {'_id': 0})

    return jsonify({"availability": list(available_slots)})


@bp.route('/get_timeslots', methods=['GET'])
def get_timeslots():
    selected_date = request.args.get('date')

    if not selected_date:
        return jsonify({"message": "Date is required"}), 400

    try:
        datetime.datetime.strptime(selected_date, '%Y-%m-%d')
    except ValueError:
        return jsonify({"message": "Invalid date format"}), 400

    available_slots = times.find({"date": selected_date},
                                 {"dentist_email": 1, "time_slots": 1, "_id": 0})

    available_slots_list = list(available_slots)
    json_slots = json_util.dumps(available_slots_list)

    return jsonify({"available_slots": json_slots})
