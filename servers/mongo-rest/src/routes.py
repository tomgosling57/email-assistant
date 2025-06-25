from fastapi import APIRouter, HTTPException
from .database import get_users_collection
from .models import User, UserCreate, PyObjectId
from bson import ObjectId

router = APIRouter()

@router.get("/users", response_model=list[User])
async def list_users():
    users = []
    for user in get_users_collection().find():
        user["_id"] = str(user["_id"]) # Convert ObjectId to string for Pydantic
        users.append(user)
    return users

@router.get("/users/{user_id}", response_model=User)
async def get_user(user_id: str):
    if not ObjectId.is_valid(user_id):
        raise HTTPException(status_code=400, detail="Invalid user ID")
    
    user = get_users_collection().find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user["_id"] = str(user["_id"]) # Convert ObjectId to string for Pydantic
    return user

@router.post("/users", response_model=User, status_code=201)
async def create_user(user: UserCreate):
    user_dict = user.model_dump(by_alias=True, exclude_unset=True)
    result = get_users_collection().insert_one(user_dict)
    created_user = get_users_collection().find_one({"_id": result.inserted_id})
    if created_user:
        created_user["_id"] = str(created_user["_id"]) # Convert ObjectId to string for Pydantic
        return created_user
    raise HTTPException(status_code=500, detail="Failed to create user")

@router.put("/users/{user_id}", response_model=User)
async def update_user(user_id: str, user: UserCreate):
    if not ObjectId.is_valid(user_id):
        raise HTTPException(status_code=400, detail="Invalid user ID")
    
    user_dict = user.model_dump(by_alias=True, exclude_unset=True)
    result = get_users_collection().update_one(
        {"_id": ObjectId(user_id)},
        {"$set": user_dict}
    )
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
    updated_user = get_users_collection().find_one({"_id": ObjectId(user_id)})
    if updated_user:
        updated_user["_id"] = str(updated_user["_id"]) # Convert ObjectId to string for Pydantic
        return updated_user
    raise HTTPException(status_code=500, detail="Failed to update user")

@router.delete("/users/{user_id}", status_code=204)
async def delete_user(user_id: str):
    if not ObjectId.is_valid(user_id):
        raise HTTPException(status_code=400, detail="Invalid user ID")
    
    result = get_users_collection().delete_one({"_id": ObjectId(user_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
    return None