import os
from pymongo import MongoClient
from dotenv import load_dotenv
from .config import get_config

load_dotenv()
config = get_config()


mongodb_uri = config.DATABASE_URI

try:
    client = MongoClient(mongodb_uri)
    db = client.Wishlist
    users = db.users
    print("Connected to the database: ", mongodb_uri)
except Exception as e:
    print(f"Error connecting to the database: {e}")
