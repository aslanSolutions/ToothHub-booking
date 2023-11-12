from flask import Flask
from apifairy import APIFairy
from flask_marshmallow import Marshmallow
from .routes import bp as notification_bp

apifairy = APIFairy()
ma = Marshmallow()

def create_app():
    app = Flask(__name__)
    app.config['APIFAIRY_TITLE'] = 'Notification API'
    app.config['APIFAIRY_VERSION'] = '1.0'
    apifairy.init_app(app)
    ma.init_app(app)
    
    app.register_blueprint(notification_bp)

    return app