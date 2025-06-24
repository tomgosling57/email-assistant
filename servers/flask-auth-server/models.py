from clients.mongodb_client import MongoDBClient
from config import Config
from flask_login import UserMixin

from dotenv import load_dotenv
import os

load_dotenv()

class User(UserMixin):
    _mongo_client = None

    def __init__(self, username, hashed_password):
        self.username = username
        self.hashed_password = hashed_password

    def to_dict(self):
        return {"username": self.username, "password": self.hashed_password}

    @staticmethod
    def set_mongo_client(client):
        User._mongo_client = client

    @staticmethod
    def get_collection():
        if User._mongo_client is None:
            raise Exception("MongoDBClient not initialized. Call User.set_mongo_client() first.")
        return User._mongo_client

    # Flask-Login integration
    def get_id(self):
        return self.username

    def is_active(self):
        return True

    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return False

    @staticmethod
    def get(user_id):
        """
        This method is used by Flask-Login's user_loader.
        It should return a User object given a user_id (username in this case).
        """
        user_data = User.find_by_username(user_id)
        if user_data:
            return User(user_data.get('username', user_id), user_data.get('password', ''))
        return None

    @staticmethod
    def find_by_username(username):
        from pymongo import MongoClient
        client = MongoClient(os.environ.get('MONGO_DB_URI', 'mongodb://mongodb:27017/'))
        db = client.test_db
        return db.users.find_one({"username": username})

    @staticmethod
    def create(username, hashed_password):
        from pymongo import MongoClient
        client = MongoClient(os.environ.get('MONGO_DB_URI', 'mongodb://mongodb:27017/'))
        db = client.test_db
        user_data = {"username": username, "password": hashed_password}
        return db.users.insert_one(user_data)

    @staticmethod
    def update_user(username, new_data):
        client = User.get_collection()
        query = {"username": username}
        return client.update_one("users", query, {"$set": new_data})

    @staticmethod
    def delete_user(username):
        client = User.get_collection()
        query = {"username": username}
        return client.delete_one("users", query)