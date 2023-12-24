import json
from .mqtt import mqtt_client
import time

def publishMessage(topic,payload):

    try:
        mqtt_client.publish(topic, json.dumps(payload),1)
        return None
    except Exception as e:
        return json({'error': str(e)}), 500


