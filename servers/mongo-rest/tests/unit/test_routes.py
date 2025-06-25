import pytest
import pytest_asyncio
from fastapi import HTTPException
from unittest.mock import Mock, patch
from bson import ObjectId

from src.main import app
from src.routes import router, list_users, get_user, create_user, update_user, delete_user
from src.database import get_users_collection
from src.models import User, UserCreate

@pytest_asyncio.fixture
async def mock_users_collection_fixture():
    with patch('src.routes.get_users_collection') as mock_get_users_collection:
        mock_collection = Mock()
        mock_get_users_collection.return_value = mock_collection
        yield mock_collection

@pytest.mark.asyncio
async def test_list_users(mock_users_collection_fixture):
    mock_users_collection = mock_users_collection_fixture
    # Setup mock data
    mock_users_collection.find.return_value = [
        {"_id": ObjectId(), "name": "User 1", "email": "user1@test.com"},
        {"_id": ObjectId(), "name": "User 2", "email": "user2@test.com"}
    ]
    
    # Call route function
    response = await list_users()
    
    # Verify response
    assert len(response) == 2
    assert all(isinstance(User.model_validate(user), User) for user in response)

@pytest.mark.asyncio
async def test_get_user_valid(mock_users_collection_fixture):
    mock_users_collection = mock_users_collection_fixture
    # Setup mock data
    user_id = ObjectId()
    mock_users_collection.find_one.return_value = {
        "_id": user_id, "name": "Test User", "email": "test@test.com"
    }
    
    # Call route function
    response = await get_user(str(user_id))
    
    # Verify response
    assert isinstance(User.model_validate(response), User)
    assert User.model_validate(response).name == "Test User"

@pytest.mark.asyncio
async def test_get_user_invalid_id(mock_users_collection_fixture):
    # Call route function with invalid ID
    with pytest.raises(HTTPException) as exc:
        await get_user("invalid_id")
    assert exc.value.status_code == 400

@pytest.mark.asyncio
async def test_get_user_not_found(mock_users_collection_fixture):
    mock_users_collection = mock_users_collection_fixture
    # Setup mock to return None (not found)
    mock_users_collection.find_one.return_value = None
    
    # Call route function
    with pytest.raises(HTTPException) as exc:
        await get_user(str(ObjectId()))
    assert exc.value.status_code == 404

# Similar tests would be added for create_user, update_user, delete_user
# Following the same pattern of mocking and verification