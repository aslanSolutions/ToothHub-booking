import json
from .mqtt import mqtt_client

topic = "notification"

def publishGetNots():
    payload = {"method": "GET"}
    try:
        mqtt_client.publish(topic, payload)
        return json({'Request send successfully': str(e)}), 200
    except Exception as e:
        return json({'error': str(e)}), 500
    

def publishGetNot(payload):
    payload["method"] = "GETOne"
    try:
        mqtt_client.publish(topic, json.dumps(payload))
        return json({'Request send successfully': str(e)}), 200
    except Exception as e:
        return json({'error': str(e)}), 500


def publishPostNot(payload):
    payload["method"] = "POST"
    try:
        mqtt_client.publish(topic, json.dumps(payload))
        return json({'Request send successfully': str(e)}), 201
    except Exception as e:
        return json({'error': str(e)}), 500


def publishDeleteNot(payload):
    payload["method"] = "DELETE"
    try:
        mqtt_client.publish(topic, json.dumps(payload))
        return json({'Request send successfully': str(e)}), 200
    except Exception as e:
        return json({'error': str(e)}), 500
