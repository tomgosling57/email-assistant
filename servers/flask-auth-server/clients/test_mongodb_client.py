import pytest
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

from dotenv import load_dotenv
import os

load_dotenv()

# MongoDB connection details (replace with your test database URI)
MONGO_URI = os.environ.get('MONGO_DB_URI', 'mongodb://mongodb:27017/')
TEST_DB_NAME = "test_db"
TEST_COLLECTION_NAME = "test_collection"

@pytest.fixture(scope="module")
def mongo_client():
    """Fixture to provide a MongoDB client for testing."""
    client = MongoClient(MONGO_URI)
    yield client
    client.close()

@pytest.mark.timeout(5)
def test_mongo_connection(mongo_client):
    """Test .if the MongoDB client can connect to the server."""
    try:
        # The ismaster command is cheap and does not require auth.
        mongo_client.admin.command('ismaster')
    except ConnectionFailure:
        pytest.fail("Failed to connect to MongoDB server")

@pytest.mark.timeout(5)
def test_insert_and_find_document(mongo_client):
    """Test inserting and retrieving a document from MongoDB."""
    db = mongo_client[TEST_DB_NAME]
    collection = db[TEST_COLLECTION_NAME]

    # Insert a test document
    test_document = {"name": "test", "value": 123}
    inserted_id = collection.insert_one(test_document).inserted_id

    # Retrieve the document
    retrieved_document = collection.find_one({"_id": inserted_id})

    assert retrieved_document is not None
    assert retrieved_document["name"] == "test"
    assert retrieved_document["value"] == 123

    # Clean up
    collection.delete_one({"_id": inserted_id})