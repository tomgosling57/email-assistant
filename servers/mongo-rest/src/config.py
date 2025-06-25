from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    MONGO_URI: str = "mongodb://mongodb:27017/"
    MONGO_DB_NAME: str = "mongo_rest_db"
    
    class Config:
        env_file = ".env"

settings = Settings()