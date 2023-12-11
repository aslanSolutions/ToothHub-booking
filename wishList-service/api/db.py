import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

mongodb_uri = os.getenv('MONGODB_URI')

try:
    client = MongoClient(mongodb_uri)
    db = client.Wishlist
    users = db.users
    print("Connected to the database.")
except Exception as e:
    print(f"Error connecting to the database: {e}")
