import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from pymongo import MongoClient
import pytest

from src.main import app
from src.database import get_db, get_users_collection
from src.config import settings

@pytest.fixture(scope="module")
def test_app():
    # Use a dedicated test database
    test_db_name = "test_mongo_rest_db"
    test_client_mongo = MongoClient(settings.MONGO_URI)
    test_db_mongo = test_client_mongo[test_db_name]

    # Drop the database to ensure a clean state before tests
    test_client_mongo.drop_database(test_db_name)
    
    # Override database connection for testing
    app.dependency_overrides[get_db] = lambda: test_db_mongo
    app.dependency_overrides[get_users_collection] = lambda: test_db_mongo["users"]
    
    with TestClient(app) as client:
        yield client
    
    # Cleanup: Drop the test database after tests
    test_client_mongo.drop_database(test_db_name)
    test_client_mongo.close()

def test_create_and_get_user(test_app):
    # Create user
    user_data = {"name": "Test User", "email": "test@test.com"}
    create_response = test_app.post("/users", json=user_data)
    assert create_response.status_code == 201
    created_user = create_response.json()
    
    # Get user
    get_response = test_app.get(f"/users/{created_user['_id']}")
    assert get_response.status_code == 200
    assert get_response.json()["name"] == "Test User"

def test_get_nonexistent_user(test_app):
    # Try to get non-existent user
    response = test_app.get("/users/507f1f77bcf86cd799439011")
    assert response.status_code == 404

# Similar tests would be added for update, delete, list operations
# Following the same pattern of API calls and assertions