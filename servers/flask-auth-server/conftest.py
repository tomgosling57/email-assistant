import pytest
from app import create_app
from models import User
from pymongo import MongoClient

@pytest.fixture(scope='session')
def app():
    """Create and configure a new app instance for each test session"""
    app = create_app()
    app.config['TESTING'] = True
    yield app

@pytest.fixture(scope='session')
def client(app):
    """A test client for the app"""
    return app.test_client()

@pytest.fixture(scope='session')
def mongo_client(app):
    """Fixture to provide MongoDB client"""
    client = MongoClient(app.config['MONGO_MCP_URL'])
    yield client
    client.close()

@pytest.fixture(autouse=True)
def setup_db(mongo_client):
    """Clean up database before each test"""
    db = mongo_client.get_database()
    db.users.drop()
    yield
    db.users.drop()