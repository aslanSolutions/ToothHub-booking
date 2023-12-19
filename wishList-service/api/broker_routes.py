import json
from .mqtt import mqtt_client
from .routes import get_wishlists


# Global variable to store the acknowledgment status
acknowledgment_received = None
acknowledgment_topic = "acknowledgment"

def publishMessage(topic,payload):
    try:
        mqtt_client.publish(topic, json.dumps(payload),0)
        return None
    except Exception as e:
        return json({'error': str(e)}), 500


# Callback to handle incoming MQTT messages
def on_message(client, userdata, msg):
    global acknowledgment_received
    try:
        payload = json.loads(msg.payload['appointment_datetime'])
        print(payload)
        whishLists = get_wishlists(payload)
        if whishLists:
            publishMessage("whishList", whishLists)
       
    except json.JSONDecodeError as e:
        print(f"Error decoding MQTT message payload: {e}")



mqtt_client.on_message = on_message
