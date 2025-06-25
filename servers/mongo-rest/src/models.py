from pydantic import BaseModel, Field, ConfigDict
from pydantic_core import core_schema
from typing import Optional, Dict
from bson import ObjectId

class PyObjectId(ObjectId):
    @classmethod
    def __get_pydantic_core_schema__(cls, _source_type, _handler):
        return core_schema.no_info_after_validator_function(
            cls.validate,
            core_schema.str_schema(),
            serialization=core_schema.to_string_ser_schema(),
        )

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

class UserBase(BaseModel):
    name: str
    email: str

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    extra_fields: Optional[Dict] = None

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True
    )