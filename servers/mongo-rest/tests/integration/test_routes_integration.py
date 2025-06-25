import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch
from bson import ObjectId

from src.main import app
from src.database import get_users_collection
from src.models import User, UserCreate

@pytest.fixture(scope="module")
def test_client_fixture():
    mock_collection = Mock()
    
    # Patch the get_users_collection function in the routes module
    with patch('src.routes.get_users_collection') as mock_get_users_collection:
        mock_get_users_collection.return_value = mock_collection
        
        with TestClient(app) as client:
            yield client, mock_collection

def test_list_users_integration(test_client_fixture):
    client, mock_db = test_client_fixture
    # Setup mock data
    mock_users = [
        {"_id": ObjectId(), "name": "User 1", "email": "user1@test.com"},
        {"_id": ObjectId(), "name": "User 2", "email": "user2@test.com"}
    ]
    mock_db.find.return_value = mock_users
    
    # Call API endpoint
    response = client.get("/users")
    
    # Verify response and database interaction
    assert response.status_code == 200
    assert len(response.json()) == 2
    mock_db.find.assert_called_once()

def test_create_user_integration(test_client_fixture):
    client, mock_db = test_client_fixture
    # Setup mock insert
    test_id = ObjectId()
    mock_db.insert_one.return_value.inserted_id = test_id
    mock_db.find_one.return_value = {
        "_id": test_id, "name": "New User", "email": "new@test.com"
    }
    
    # Call API endpoint
    user_data = {"name": "New User", "email": "new@test.com"}
    response = client.post("/users", json=user_data)
    
    # Verify response and database interaction
    assert response.status_code == 201
    assert response.json()["name"] == "New User"
    mock_db.insert_one.assert_called_once()
    mock_db.find_one.assert_called_once()

# Similar tests would be added for other routes (get_user, update_user, delete_user)
# Following the same pattern of using TestClient and mocking database interactions