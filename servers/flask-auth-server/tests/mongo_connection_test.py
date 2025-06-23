import pymongo
from pymongo import MongoClient
import sys

print(f"Using PyMongo version: {pymongo.__version__}")

try:
    # Connect using container name
    client = MongoClient('mongodb://email-assistant-mongodb-1:27017',
                       serverSelectionTimeoutMS=5000,
                       connectTimeoutMS=10000,
                       socketTimeoutMS=10000)
    print("Attempting MongoDB connection with PyMongo...")
    ping_result = client.admin.command('ping')
    print(f"MongoDB connection successful! Ping result: {ping_result}")
    sys.exit(0)
except pymongo.errors.ConnectionFailure as e:
    print(f"MongoDB connection failed: {e}")
    sys.exit(1)
except Exception as e:
    print(f"Unexpected error: {e}")
    sys.exit(2)