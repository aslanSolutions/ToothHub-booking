import os
from flask import Flask
from apifairy import APIFairy
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager
from .routes import bp
from dotenv import load_dotenv
from flask_cors import CORS
from .mqtt import mqtt_client

brokerAdress = "0169ad6feac84c25b5b11b5157be1bd8.s2.eu.hivemq.cloud"
brokerPort = 8883
apifairy = APIFairy()
ma = Marshmallow()
jwt = JWTManager() 


def create_app():
    app = Flask(__name__)

    load_dotenv()

    CORS(app)

    app.config['APIFAIRY_TITLE'] = 'Appointment API'
    app.config['APIFAIRY_VERSION'] = '1.0'

    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
    app.config['JWT_TOKEN_LOCATION'] = ['headers']

    # Set the MQTT broker address and port
    app.config['MQTT_BROKER_ADDRESS'] = brokerAdress
    app.config['MQTT_PORT'] = brokerPort

    apifairy.init_app(app)
    ma.init_app(app)
    jwt.init_app(app)

    app.register_blueprint(bp)
    # Add the MQTT client to the app context
    app.mqtt_client = mqtt_client

    # Start the MQTT client loop in a separate thread
    # Connecting the MQTT client
    mqtt_client.connect(app.config['MQTT_BROKER_ADDRESS'], app.config['MQTT_PORT'])
    mqtt_client.loop_start()


    return app