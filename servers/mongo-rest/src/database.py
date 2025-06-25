from pymongo import MongoClient
from .config import settings

client = MongoClient(settings.MONGO_URI)
db = client[settings.MONGO_DB_NAME]
users_collection = db["users"]

def get_db():
    return db

def get_users_collection():
    return users_collection