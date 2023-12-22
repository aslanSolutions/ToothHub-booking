import json
from .mqtt import mqtt_client
import time




def publishMessage(topic,payload):

    try:
        mqtt_client.publish(topic, json.dumps(payload),0)
        return None
    except Exception as e:
        return json({'error': str(e)}), 500


# Callback to handle incoming MQTT messages
def on_message(client, userdata, msg):
    try:
        topic = json.loads(msg.topic)
        if topic == 'booking/create':
            pass
        elif topic == 'booking/delete':
            pass
        else:
            pass

        payload = json.loads(msg.payload)
        print(payload)
       
    except json.JSONDecodeError as e:
        print(f"Error decoding MQTT message payload: {e}")


mqtt_client.on_message = on_message
