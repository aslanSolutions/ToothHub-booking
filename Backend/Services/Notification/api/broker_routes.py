import json
from . import mqtt_client

topic = "notification"

def publishGetNots():
    payload = {"method": "GET"}
    mqtt_client.publish(topic, payload)

def publishGetNot(payload):
    payload["method"] = "GETOne"
    mqtt_client.publish(topic, json.dumps(payload))

def publishPostNot(payload):
    payload["method"] = "POST"
    mqtt_client.publish(topic, json.dumps(payload))


def publishDeleteNot(payload):
    payload["method"] = "DELETE"
    mqtt_client.publish(topic, json.dumps(payload))
