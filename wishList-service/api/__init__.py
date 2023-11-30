from flask import Flask
from apifairy import APIFairy
from flask_marshmallow import Marshmallow
from .routes import bp

apifairy = APIFairy()
ma = Marshmallow()

def create_app():
    app = Flask(__name__)
    app.config['APIFAIRY_TITLE'] = 'Wishlist API'
    app.config['APIFAIRY_VERSION'] = '1.0'

    # Initialize APIFairy, Marshmallow
    apifairy.init_app(app)
    ma.init_app(app)

    # Register the dentsit blueprint
    app.register_blueprint(bp)

    return app