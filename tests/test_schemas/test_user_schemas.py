import pytest
from pydantic import ValidationError
from datetime import datetime
from app.schemas.user_schemas import UserBase, UserCreate, UserUpdate, UserResponse, UserListResponse, LoginRequest

@pytest.fixture
def user_response_data():
    return {
        "id": "unique-id-string",
        "username": "testuser",
        "email": "test@example.com",
        "last_login_at": datetime.now(),
        "created_at": datetime.now(),
        "updated_at": datetime.now(),
        "links": []
    }

# Function to extract example data from a Pydantic model
def get_model_example_data(model):
    return model.schema()['example']

# Tests for UserBase
def test_user_base_valid():
    example_data = get_model_example_data(UserBase)
    user = UserBase(**example_data)
    assert user.username == example_data["username"]
    assert user.email == example_data["email"]

# Tests for UserCreate
def test_user_create_valid():
    example_data = get_model_example_data(UserCreate)
    user = UserCreate(**example_data)
    assert user.username == example_data["username"]
    assert user.password == example_data["password"]

# Tests for UserUpdate
def test_user_update_partial():
    example_data = get_model_example_data(UserUpdate)
    partial_data = {"email": example_data["email"]}
    user_update = UserUpdate(**partial_data)
    assert user_update.email == partial_data["email"]

# Tests for UserResponse
def test_user_response_datetime(user_response_data):
    user = UserResponse(**user_response_data)
    assert user.last_login_at == user_response_data["last_login_at"]
    assert user.created_at == user_response_data["created_at"]
    assert user.updated_at == user_response_data["updated_at"]

# Tests for LoginRequest
def test_login_request_valid():
    example_data = get_model_example_data(LoginRequest)
    login = LoginRequest(**example_data)
    assert login.username == example_data["username"]
    assert login.password == example_data["password"]

# Parametrized tests for username and email validation
@pytest.mark.parametrize("username", ["test_user", "test-user", "testuser123", "123test"])
def test_user_base_username_valid(username):
    example_data = get_model_example_data(UserBase)
    example_data["username"] = username
    user = UserBase(**example_data)
    assert user.username == username

@pytest.mark.parametrize("username", ["test user", "test?user", "", "us"])
def test_user_base_username_invalid(username):
    example_data = get_model_example_data(UserBase)
    example_data["username"] = username
    with pytest.raises(ValidationError):
        UserBase(**example_data)
