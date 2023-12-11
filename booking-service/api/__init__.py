import os
from flask import Flask
from apifairy import APIFairy
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager
from .routes import bp
from dotenv import load_dotenv
from flask_cors import CORS

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

    apifairy.init_app(app)
    ma.init_app(app)
    jwt.init_app(app)

    app.register_blueprint(bp)

    return app