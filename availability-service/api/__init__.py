from flask import Flask
from apifairy import APIFairy
from flask_cors import CORS
from flask_marshmallow import Marshmallow
from .routes import bp
from .mqtt import mqtt_client
from .config import get_config

apifairy = APIFairy()
ma = Marshmallow()

def create_app():
    app = Flask(__name__)

    CORS(app)
    app.config.from_object(get_config())

    apifairy.init_app(app)
    ma.init_app(app)

    app.register_blueprint(bp)

    # Add the MQTT client to the app context
    app.mqtt_client = mqtt_client

    # Start the MQTT client loop in a separate thread
    # Connecting the MQTT client
    mqtt_client.connect(app.config['MQTT_BROKER_ADDRESS'], app.config['MQTT_PORT'])
    mqtt_client.loop_start()
    

    return app