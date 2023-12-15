import json
from .mqtt import mqtt_client

def publishMessage(topic,payload):
    try:
        mqtt_client.publish(topic, json.dumps(payload),0)
        return None
    except Exception as e:
        return json({'error': str(e)}), 500

