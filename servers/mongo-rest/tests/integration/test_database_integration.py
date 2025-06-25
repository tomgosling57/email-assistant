import pytest
from pymongo import MongoClient
from pymongo import MongoClient
import pytest

from src.database import get_db, get_users_collection
from src.config import settings

@pytest.fixture(scope="module")
def test_db_integration():
    # Use a dedicated test database for integration tests
    test_db_name = "test_mongo_rest_integration_db"
    test_client = MongoClient(settings.MONGO_URI)
    test_db = test_client[test_db_name]

    # Drop the database to ensure a clean state before tests
    test_client.drop_database(test_db_name)
    
    yield test_db
    
    # Cleanup: Drop the test database after tests
    test_client.drop_database(test_db_name)
    test_client.close()

def test_get_db_integration(test_db_integration):
    db = get_db()
    assert db.name == settings.MONGO_DB_NAME # Should be the actual app db name
    
def test_get_users_collection_integration(test_db_integration):
    collection = get_users_collection()
    assert collection.name == "users"
    assert collection.database.name == settings.MONGO_DB_NAME # Should be the actual app db name
