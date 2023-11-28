import os
from pymongo import MongoClient
from flask_dotenv import DotEnv

DotEnv()

mongodb_uri = "mongodb+srv://ali:ali@aslan.im1wsjq.mongodb.net/"


try:
    client = MongoClient(mongodb_uri)
    db = client.availability_times
    times = db.times
    print("Connected to the database.")
except Exception as e:
    print(f"Error connecting to the database: {e}")

