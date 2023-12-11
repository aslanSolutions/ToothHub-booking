from flask import Flask
from apifairy import APIFairy
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager
from .routes import bp
from flask_cors import CORS
import os
from dotenv import load_dotenv


apifairy = APIFairy()
ma = Marshmallow()
jwt = JWTManager()  # Initialize JWTManager

def create_app():
    
    app = Flask(__name__)
    load_dotenv()

    app.config['APIFAIRY_TITLE'] = 'Wishlist API'
    app.config['APIFAIRY_VERSION'] = '1.0'

    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
    app.config['JWT_TOKEN_LOCATION'] = ['headers']

    CORS(app)

    apifairy.init_app(app)
    ma.init_app(app)
    jwt.init_app(app)

    # Register the blueprint
    app.register_blueprint(bp)

    return app
