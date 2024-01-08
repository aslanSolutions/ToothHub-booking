from flask import Flask
from apifairy import APIFairy
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager
from .routes import bp
from flask_cors import CORS
import os
from dotenv import load_dotenv
from .mqtt import mqtt_client
from .broker_routes import publishMessage
from .config import get_config



brokerAdress = "0169ad6feac84c25b5b11b5157be1bd8.s2.eu.hivemq.cloud"
brokerPort = 8883

apifairy = APIFairy()
ma = Marshmallow()
jwt = JWTManager()  # Initialize JWTManager

def create_app():
    
    app = Flask(__name__)
    load_dotenv()
    app.config.from_object(get_config())


    CORS(app)

    apifairy.init_app(app)
    ma.init_app(app)
    jwt.init_app(app)
    app.mqtt_client = mqtt_client

    # Register the blueprint
    app.register_blueprint(bp)

    # Start the MQTT client loop in a separate thread
    # Connecting the MQTT client
    mqtt_client.connect(app.config['MQTT_BROKER_ADDRESS'], app.config['MQTT_PORT'])
    mqtt_client.loop_start()

    return app
