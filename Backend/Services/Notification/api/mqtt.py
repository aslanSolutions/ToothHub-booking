import json
import paho.mqtt.client as mqtt
from flask_socketio import SocketIO

mqtt_client = mqtt.Client()
socketio = SocketIO()

def on_connect(client, userdata, rc):
    if rc == 0:
        print("Connected with result code " + str(rc))
        print("User data: " + str(userdata))
        client.subscribe("topic/1")  # Topic to be changed
    else:
        print("Connection failed with code " + str(rc))

def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload)
        method = payload.get("method")

        if method in ["GETOne", "GET", "POST", "DELETE"]:
            socketio.emit('notification_response', {'method': method, 'payload': payload})

    except json.JSONDecodeError as e:
        print("Error decoding JSON:", e)

mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message
