import pytest
from app import create_app
from pymongo import MongoClient

@pytest.fixture(scope='session')
def app():
    app = create_app()
    app.config['TESTING'] = True
    app.config['MONGO_URI'] = 'mongodb://localhost:27017/test_db'
    return app

@pytest.fixture(scope='module')
def flask_test_client(app):
    with app.test_client() as client:
        yield client

@pytest.fixture(scope='function')
def setup_db(app):
    """Setup test database before each test"""
    client = MongoClient(app.config['MONGO_URI'])
    db = client.get_database()
    db.users.drop()
    yield
    db.users.drop()