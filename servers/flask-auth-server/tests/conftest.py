import pytest
import sys
import os



from factory import create_app
from clients.mongodb_client import MongoDBClient
from models import User

@pytest.fixture(scope='module')
def app():
    app = create_app()
    app.config['TESTING'] = True
    yield app

@pytest.fixture(scope='module')
def setup_users(flask_test_client):
    """
    Fixture to ensure a clean state for user data before running tests.
    Clears the 'users' collection in the test database.
    """
    mongo_client = MongoDBClient(base_url=flask_test_client.application.config['MONGO_MCP_URL'])
    User.set_mongo_client(mongo_client)
    
    # Clear the users collection before tests using User model
    test_user = User("test_user", "test_password")
    test_user.delete_user("test_user")  # Clears if exists
    print(f"Cleared users collection in {flask_test_client.application.config['MONGO_MCP_URL']}")
    yield
    # Teardown: Clean up any created users after tests
    test_user.delete_user("test_user")  # Ensure clean state
    print(f"Cleared users collection in {flask_test_client.application.config['MONGO_MCP_URL']} during teardown")


@pytest.fixture(scope='module')
def flask_test_client(app):
    """
    Fixture that provides a test client for the Flask app.
    """
    with app.test_client() as client:
        yield client