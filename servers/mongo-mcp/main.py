from fastapi import FastAPI, HTTPException
from pymongo import MongoClient
import os

app = FastAPI()

# MongoDB connection details
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
DB_NAME = os.getenv("DB_NAME", "testdb")

client = None
db = None

@app.on_event("startup")
async def startup_db_client():
    global client, db
    try:
        client = MongoClient(MONGO_URI)
        db = client[DB_NAME]
        # The ping command is cheap and does not require auth.
        client.admin.command('ping')
        print("MongoDB connection successful!")
    except Exception as e:
        print(f"Could not connect to MongoDB: {e}")
        # In a real application, you might want to exit or handle this more gracefully
        raise HTTPException(status_code=500, detail=f"Database connection error: {e}")

@app.on_event("shutdown")
async def shutdown_db_client():
    if client:
        client.close()
        print("MongoDB connection closed.")

@app.get("/")
async def read_root():
    return {"message": "mongo-mcp is running!"}

@app.get("/test-db-connection")
async def test_db_connection():
    if db:
        try:
            # Attempt to list collections to verify connection
            db.list_collection_names()
            return {"status": "success", "message": "Successfully connected to MongoDB and performed a test operation."}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"MongoDB operation failed: {e}")
    else:
        raise HTTPException(status_code=500, detail="MongoDB client not initialized.")