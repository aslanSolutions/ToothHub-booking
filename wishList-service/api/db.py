import os
from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve MongoDB URI from environment variable
mongodb_uri = os.getenv('MONGODB_URI')  # Use the variable 'mongodb_uri' here

try:
    client = MongoClient(mongodb_uri, tlsAllowInvalidCertificates=True)  # Use the 'mongodb_uri' variable
    db = client.Wishlist
    users = db.users
    print("Connected to the database.")
except Exception as e:
    print(f"Error connecting to the database: {e}")
