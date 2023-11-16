import json
import paho.mqtt.client as mqtt
from flask_socketio import SocketIO

mqtt_client = mqtt.Client(client_id="patient_side", protocol=mqtt.MQTTv311)
mqtt_client.tls_set(tls_version=mqtt.ssl.PROTOCOL_TLS)
socketio = SocketIO()

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected with result code " + str(rc))
        print("User data: " + str(userdata))
        client.subscribe("patient")  # Topic to be changed
        mqtt_client.publish("patient", "Aslan server sending a new patient")
    else:
        print("Connection failed with code " + str(rc))

def on_message(client, userdata, msg):
    try:
        print("Message resived: ", msg.topic ,", ",msg.payload.decode("utf-8"))
        #if method in ["GETOne", "GET", "POST", "DELETE"]:
        #    socketio.emit('notification_response', {'method': method, 'payload': payload})

    except json.JSONDecodeError as e:
        print("Error decoding JSON:", e)

mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message
mqtt_client.username_pw_set("group7", "Group777")