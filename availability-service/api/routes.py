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

    for time_slot in data['time_slots']:
        time_slot.setdefault('booked', False)

    existing_entry = times.find_one(
        {'dentist_email': dentist_email, 'date': date})
    if existing_entry:
        new_time_slots = data['time_slots']
        times.update_one({'_id': existing_entry['_id']}, {
                         '$set': {'time_slots': new_time_slots}})
        updated_entry = times.find_one({'_id': existing_entry['_id']})
        date_time = {"date": updated_entry["date"]}
        message_json = json_util.dumps(date_time)
        publishMessage('availability', message_json)
        return jsonify({"message": "Availability updated successfully", "availability": json_util.dumps(updated_entry)}), 200
    else:
        result = times.insert_one(data)
        new_availability_id = result.inserted_id
        created_availability = times.find_one({'_id': new_availability_id})
        date_time = {"date": created_availability["date"]}
        publishMessage('availability', json_util.dumps(date_time))
        return jsonify({"message": "Availability set successfully", "availability": json_util.dumps(created_availability)}), 201



@bp.route('/get_availability', methods=['GET'])
def get_availability():
    dentist_email = request.args.get('dentist_email')
    booked_status = request.args.get('booked', default='false').lower() == 'true' 

    if not dentist_email:
        return jsonify({"message": "Dentist email is required"}), 400

    query = {'dentist_email': dentist_email}

    available_slots = times.find(query, {'_id': 0})

    filtered_slots = []
    for slot in available_slots:
        filtered_time_slots = [ts for ts in slot['time_slots'] if ts['booked'] == booked_status]
        if filtered_time_slots:
            slot['time_slots'] = filtered_time_slots
            filtered_slots.append(slot)

    return jsonify({"availability": filtered_slots})


@bp.route('/get_timeslots', methods=['GET'])
def get_timeslots():
    selected_date = request.args.get('date')
    booked_param = request.args.get('booked', 'false').lower() == 'true'

    if not selected_date:
        return jsonify({"message": "Date is required"}), 400

    try:
        datetime.strptime(selected_date, '%Y-%m-%d') 
    except ValueError:
        return jsonify({"message": "Invalid date format"}), 400

    query = {"date": selected_date, "time_slots.booked": booked_param}

    available_slots = times.find(query, {"dentist_email": 1, "time_slots": 1, "_id": 0})

    # Filter out booked timeslots from each document's timeslot list
    available_slots_list = []
    for slot in available_slots:
        slot['time_slots'] = [ts for ts in slot['time_slots'] if ts['booked'] == booked_param]
        available_slots_list.append(slot)

    json_slots = json_util.dumps(available_slots_list)

    return jsonify({"available_slots": json_slots})

# For higher performance we use function call when a message is received from the broker.


def deleteAppointment(data):
    try:

        print(f"Date: ", data)
        dentist_email = data['dentist_email']
        # Format the date correctly
        appointmentDate = datetime.strptime(data['appointment_datetime'], '%Y-%m-%d %H:%M:%S').isoformat()
        query = {
            'dentist_email': dentist_email,
            "time_slots": {
                "$elemMatch": {
                    "start_time": appointmentDate,
                }
            }
        }

        result = times.update_one(query, {'$set': {'time_slots.$.booked': False}})
        print(f"Result:" , result)
        if result.modified_count > 0:
            data['acknowledgment'] = 'True'
            data['topic'] = 'booking/delete'
            publishMessage('acknowledgment', json.dumps(data))
            publishMessage('availability', json_util.dumps(data))
        else:
            data['acknowledgment'] = 'False'
            publishMessage('acknowledgment', json.dumps(data))
    except Exception as e:
        print({"error": str(e)})


def checkForAvailability(payload):
    try:
        json_payload = json.loads(payload)
        appointmentDate = json_payload['appointment_datetime']
        print(f"Json:", appointmentDate)
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

        if available_slots:
            print("Found available slot: ", available_slots)
            json_payload['acknowledgment'] = 'True'
            json_payload['topic'] = 'booking/create'
            publishMessage('acknowledgment', json.dumps(json_payload))

        else:
            print("No available_slots were found")
            json_payload['acknowledgment'] = 'False'
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
            publishMessage('acknowledgment', json_payload)
        else:
            json_payload['acknowledgment'] = 'False'
            publishMessage('acknowledgment', json_payload)
    except Exception as e:
        print({"error": str(e)})


def handleConfirmation(data):
    dentist_email = data['dentist_email']
    appointmentDate = data['appointment_datetime']

    if data['status'] == "success":
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
        if topic == 'booking/create':
            print("Create request resived...")
            try:
                checkForAvailability(json_payload)
            except Exception as e:
                print({"error": str(e)})
        elif topic == 'booking/delete':
            print("Delete request resived...")
            last_payload = json.loads(json_payload)
            deleteAppointment(last_payload)
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
