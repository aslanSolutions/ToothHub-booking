from flask import Flask
from apifairy import APIFairy
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager
from .routes import bp

apifairy = APIFairy()
ma = Marshmallow()
jwt = JWTManager()  # Initialize JWTManager

def create_app():
    app = Flask(__name__)
    app.config['APIFAIRY_TITLE'] = 'Wishlist API'
    app.config['APIFAIRY_VERSION'] = '1.0'

    # JWT configuration
    app.config['JWT_SECRET_KEY'] = 'secret_key'  # Change this to a secret key of your choice
    app.config['JWT_TOKEN_LOCATION'] = ['headers']  # JWT tokens will be located in the headers

    # Initialize extensions
    apifairy.init_app(app)
    ma.init_app(app)
    jwt.init_app(app)  # Initialize the JWT extension

    # Register the blueprint
    app.register_blueprint(bp)

    return app
