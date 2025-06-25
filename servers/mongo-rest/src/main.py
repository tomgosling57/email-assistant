from fastapi import FastAPI
from .routes import router
from .database import get_db

app = FastAPI(
    title="Mongo-REST API",
    description="REST API for MongoDB operations",
    version="1.0.0"
)

app.include_router(router, prefix="")

@app.on_event("startup")
async def startup_db_client():
    # Test the connection
    get_db().command('ping')
    print("Connected to MongoDB!")