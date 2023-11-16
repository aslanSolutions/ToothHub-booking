from flask import Flask
from apifairy import APIFairy
from flask_marshmallow import Marshmallow
from .routes import bp as notification_bp
from .mqtt import mqtt_client, socketio
from pymongo import MongoClient
client = MongoClient('localhost', 27017)

apifairy = APIFairy()
ma = Marshmallow()

brokerAdress = "0169ad6feac84c25b5b11b5157be1bd8.s2.eu.hivemq.cloud"
brokerPort = 8883

def create_app():
    app = Flask(__name__)
    app.config['APIFAIRY_TITLE'] = 'Notification API'
    app.config['APIFAIRY_VERSION'] = '1.0'

    # Initialize APIFairy, Marshmallow, and Socketio
    apifairy.init_app(app)
    ma.init_app(app)
    socketio.init_app(app)
    db = client.flask_db
    todos = db.todos  
    # Register the notification blueprint
    app.register_blueprint(notification_bp)

    # Set the MQTT broker address and port
    app.config['MQTT_BROKER_ADDRESS'] = brokerAdress
    app.config['MQTT_PORT'] = brokerPort

    # Add the MQTT client to the app context
    app.mqtt_client = mqtt_client

    # Start the MQTT client loop in a separate thread
    # Connecting the MQTT client
    mqtt_client.connect(app.config['MQTT_BROKER_ADDRESS'], app.config['MQTT_PORT'])
    mqtt_client.loop_start()

    return app
