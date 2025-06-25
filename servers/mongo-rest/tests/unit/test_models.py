import pytest
from bson import ObjectId
from pydantic import ValidationError

from src.models import PyObjectId, User, UserCreate

def test_pyobjectid_valid():
    # Test valid ObjectId string
    valid_id = str(ObjectId())
    pyoid = PyObjectId.validate(valid_id)
    assert isinstance(pyoid, ObjectId)

def test_pyobjectid_invalid():
    # Test invalid ObjectId string
    with pytest.raises(ValueError, match="Invalid ObjectId"):
        PyObjectId.validate("invalid_id")

def test_user_model_validation():
    # Test valid user creation
    user = User(
        id=str(ObjectId()),
        name="Test User",
        email="test@example.com"
    )
    assert user.name == "Test User"
    assert user.email == "test@example.com"

def test_user_missing_required_fields():
    # Test missing required fields
    with pytest.raises(ValidationError):
        User(name="Test User")  # Missing email

def test_usercreate_model_validation():
    # Test valid UserCreate
    user = UserCreate(
        name="Test User",
        email="test@example.com"
    )
    assert user.name == "Test User"
    assert user.email == "test@example.com"

def test_usercreate_missing_required_fields():
    # Test missing required fields
    with pytest.raises(ValidationError):
        UserCreate(name="Test User")  # Missing email