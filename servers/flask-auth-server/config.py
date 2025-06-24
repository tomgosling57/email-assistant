
from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'a_very_secret_key_that_should_be_changed_in_production'
    STREAMLIT_APP_URL = os.environ.get('STREAMLIT_APP_URL') or 'http://localhost:8501'
    MONGO_MCP_URL = os.environ.get('MONGO_MCP_URL') or 'http://mongo_mcp:8002'
    TESTING = False # Default to False

class TestConfig(Config):
    TESTING = True
    MONGO_MCP_URL = f"mongodb://{os.environ.get('DOCKER_NAMESPACE')}-mongodb-1:27017/test_db" # Use container name.