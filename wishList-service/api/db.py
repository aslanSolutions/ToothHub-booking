import os
from pymongo import MongoClient
from flask_dotenv import DotEnv

DotEnv()

MONGODB_URI = "mongodb+srv://ali:ali@aslan.im1wsjq.mongodb.net/"


try:
    client = MongoClient(MONGODB_URI)
    db = client.Wishlist
    users = db.users
    print("Connected to the database.")
except Exception as e:
    print(f"Error connecting to the database: {e}")

