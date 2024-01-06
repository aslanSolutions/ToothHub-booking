import json
from .mqtt import mqtt_client
from .routes import get_wishlists
from flask import current_app as app
import json



# Global variable to store the acknowledgment status
acknowledgment_received = None
acknowledgment_topic = "acknowledgment"

def publishMessage(topic,payload):
    try:
        mqtt_client.publish(topic, json.dumps(payload),0)
        return None
    except Exception as e:
        return json({'error': str(e)}), 500


def on_message(client, userdata, msg):
    global acknowledgment_received
    try:
        decoded_payload = msg.payload.decode('utf-8')
        payload = json.loads(decoded_payload)
        if isinstance(payload, str):
            payload = json.loads(payload)

        if isinstance(payload, dict) and 'date' in payload:
            date = payload['date']
            wishLists = get_wishlists(date)
            if wishLists:
                response_payload = {
                    "wishLists": wishLists,
                    "topic": 'wishList',
                    "appointment_datetime": date,
                    "acknowledgment": True
                }
                publishMessage("wishList", json.dumps(response_payload))
            else:
                print("No wishlists found for the date:", date)
        else:
            print("Invalid payload format. Expected a dictionary with a 'date' key.")

    except json.JSONDecodeError as e:
        print(f"Error decoding MQTT message payload: {e}")
    except Exception as e:
        print(f"General error in message processing: {e}")




mqtt_client.on_message = on_message
