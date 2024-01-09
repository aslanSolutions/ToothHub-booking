import os
from dotenv import load_dotenv
load_dotenv()


class Config:
    APIFAIRY_TITLE = 'Availible API'
    APIFAIRY_VERSION = '1.0'
    MQTT_BROKER_ADDRESS = "0169ad6feac84c25b5b11b5157be1bd8.s2.eu.hivemq.cloud"
    MQTT_PORT = 8883
    CLEAN_SESSION = True

class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = True
    DATABASE_URI = 'mongodb://localhost:27017'
    PORT=5004

class ProductionConfig(Config):
    MONGO_DB_USERNAME = os.getenv('MONGO_DB_USERNAME', 'default_username')
    MONGO_DB_PASSWORD = os.getenv('MONGO_DB_PASSWORD', 'default_password')
    DATABASE_PORT =  os.getenv('DATABASE_PORT', '27017')
    DATABASE_URI = f'mongodb+srv://{MONGO_DB_USERNAME}:{MONGO_DB_PASSWORD}@aslan.im1wsjq.mongodb.net/{DATABASE_PORT}'
    DEBUG = False
    TESTING = False
    PORT=5004

def get_config():
    envi = os.environ.get('FLASK_ENV', 'development')
    if envi == 'production':
        return ProductionConfig
    else:
        return DevelopmentConfig
