import json
from flask import Blueprint, jsonify, request
import timedelta
from .schema import TimeSlotSchema, AvailabilityTimeSchema
from .db import times
from bson import json_util
from datetime import datetime, timedelta
from .broker_routes import publishMessage, mqtt_client
from bson import ObjectId


bp = Blueprint('availability', __name__, url_prefix='/availability')


@bp.route('/', methods=['POST'])
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
        publishMessage('availability', json_util.dumps(updated_entry))
        return jsonify({"message": "Availability updated successfully", "availability": json_util.dumps(updated_entry)}), 200
    else:
        result = times.insert_one(data)
        new_availability_id = result.inserted_id
        created_availability = times.find_one({'_id': new_availability_id})
        publishMessage('availability', json_util.dumps(updated_entry))
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

# For higher performance we use function call when a message is received from the broker.


def deleteAppointment(payload):
    try:
        json_payload = json.loads(payload)
        object_id = ObjectId(json_payload['appointment_id'])
        try:
            available_slots = times.delete_one({
                '_id': object_id
            })
        except Exception as e:
            print(e)
        if available_slots.deleted_count > 0:
            json_payload['acknowledgment'] = 'False'
            json_payload['topic'] = 'delete/booking'
            publishMessage('acknowledgment', json_payload)
        else:
            json_payload['acknowledgment'] = 'True'
            publishMessage('acknowledgment', json_payload)
    except Exception as e:
        print({"error": str(e)})


def checkForAvailability(payload):
    try:
        json_payload = json.loads(payload)
        appointmentDate = json_payload['appointment_datetime']
        try:
            available_slots = times.find_one({
                "time_slots": {
                    "$elemMatch": {
                        "start_time": appointmentDate,
                        "booked": False
                    }
                }
            })
        except Exception as e:
            print({"error": str(e)})

        print("Slots:", available_slots)

        if available_slots:
            print("Found available slot: ", available_slots)
            json_payload['acknowledgment'] = 'True'
            publishMessage('acknowledgment', json.dumps(json_payload))

        else:
            print("No available_slots were found")
            json_payload['acknowledgment'] = 'False'
            json_payload['topic'] = 'create/booking'
            publishMessage('acknowledgment', json.dumps(json_payload))
    except Exception as e:
        print({"error": str(e)})


def updateAppointment(payload):
    try:
        json_payload = json.loads(payload)
        object_id = ObjectId(json_payload.pop('id'))
        try:
            available_slots = times.update_one(
                {"_id": object_id},
                {'$set': json_payload.pop('correlation_id')}
            )
        except Exception as e:
            print(e)

        if available_slots.modified_count > 0:
            json_payload['acknowledgment'] = 'True'
            json_payload['topic'] = 'update/booking'
            print("Data", json_payload)
            publishMessage('acknowledgment', json_payload)
        else:
            json_payload['acknowledgment'] = 'False'
            publishMessage('acknowledgment', json_payload)
    except Exception as e:
        print({"error": str(e)})


def handleConfirmation(data):
    dentist_email = data['dentist_email']
    appointmentDate = data['appointment_datetime']
    print("Got data:", data)

    if data['status'] == "success":
        # Find the corresponding availability entry and update
        result = times.update_one(
            {
                'dentist_email': dentist_email,
                "time_slots": {
                    "$elemMatch": {
                        "start_time": appointmentDate,
                    }
                }
            },
            {'$set': {'time_slots.$.booked': True}}
        )

        if result.modified_count > 0:
            print("Time slot marked as booked.")
        else:
            print("Failed to mark time slot as booked.")
    else:
        print(f"Not confirmed!")


# Callback to handle incoming MQTT messages
def on_message(client, userdata, msg):
    try:
        topic = msg.topic
        payload = (msg.payload.decode("utf-8"))
        json_payload = json.loads(payload)
        print(json_payload)
        if topic == 'booking/create':
            print("Create request resived...")
            try:
                checkForAvailability(json_payload)
            except Exception as e:
                print({"error": str(e)})
        elif topic == 'booking/delete':
            print("Delete request resived...")
            deleteAppointment(json_payload)
        elif topic == 'booking/update':
            print("Update request resived...")
            updateAppointment(json_payload)
        elif topic == 'booking/confirm':
            last_payload = json.loads(json_payload)
            handleConfirmation(last_payload)
        else:
            print("payload resived but nothing to do")
    except Exception as e:
        print({"error": str(e)})


mqtt_client.on_message = on_message
