from flask import Flask
from apifairy import APIFairy
from flask_marshmallow import Marshmallow
from .routes import bp as notification_bp
import paho.mqtt.client as mqtt

apifairy = APIFairy()
ma = Marshmallow()
mqtt_client = mqtt.Client()

brokerAdress = None
brokerPort = None

# Callback function to confirm connection with the broker
def on_connect(client, userdata, rc):
    if rc == 0:
        print("Connected with result code " + str(rc))
        print("User data: " + str(userdata))
        client.subscribe("topic/1") # Topic to be changed
    else:
        print("Connection failed with code "+str(rc))

# Callback function for when a Publish message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))
    

def create_app():
    app = Flask(__name__)
    app.config['APIFAIRY_TITLE'] = 'Notification API'
    app.config['APIFAIRY_VERSION'] = '1.0'
    
    # Initialize APIFairy and Marshmallow
    apifairy.init_app(app)
    ma.init_app(app)
    
    # Register the notification blueprint
    app.register_blueprint(notification_bp)
    
    # Set the MQTT broker address and port
    app.config['MQTT_BROKER_ADDRESS'] = brokerAdress
    app.config['MQTT_PORT'] = brokerPort
    
    # Connecting the MQTT client
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message
    mqtt_client.connect(app.config['MQTT_BROKER_ADDRESS'], app.config['MQTT_PORT'])
    
    # Add the MQTT client to the app context
    app.mqtt_client = mqtt_client
    
    # Start the MQTT client loop in a separate thread
    mqtt_client.loop_start()

    return app
