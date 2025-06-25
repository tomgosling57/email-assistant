import pytest
from unittest.mock import Mock, patch
from pymongo.database import Database
from pymongo.collection import Collection

from src.database import get_db, get_users_collection

@pytest.fixture
def mock_database_objects():
    with patch('src.database.client') as mock_client, \
         patch('src.database.db') as mock_db, \
         patch('src.database.users_collection') as mock_users_collection:
        
        # Configure mocks to return themselves for chaining
        mock_client.return_value = mock_client
        mock_db.return_value = mock_db
        mock_users_collection.return_value = mock_users_collection
        
        yield mock_client, mock_db, mock_users_collection

def test_get_db(mock_database_objects):
    _, mock_db, _ = mock_database_objects
    db = get_db()
    assert db is mock_db

def test_get_users_collection(mock_database_objects):
    _, _, mock_users_collection = mock_database_objects
    collection = get_users_collection()
    assert collection is mock_users_collection