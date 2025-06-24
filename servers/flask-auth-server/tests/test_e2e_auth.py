import pytest
import json
from clients.mongodb_client import MongoDBClient
from models import User

@pytest.mark.timeout(10)
def test_successful_registration(setup_users, flask_test_client):
    """
    Test case for successful user registration.
    """
    username = "e2e_test_user_register"
    password = "e2e_password123"
    
    # Ensure user does not exist from previous runs
    flask_test_client.post("/auth/delete_user", json={"username": username})

    response = flask_test_client.post("/auth/register", data={
        "username": username,
        "password": password,
        "confirm_password": password
    })
    assert response.status_code == 200
    assert b"Registration successful! Please log in." in response.data

    # Verify user can log in after registration
    login_response = flask_test_client.post("/auth/login", data={
        "username": username,
        "password": password
    })
    assert login_response.status_code == 200
    assert b"Login successful!" in login_response.data # Assuming a success message on dashboard

@pytest.mark.timeout(10)
def test_registration_existing_username(setup_users, flask_test_client):
    """
    Test case for registration with an existing username.
    """
    username = "e2e_existing_user"
    password = "e2e_password123"

    # Register the user first
    flask_test_client.post("/auth/register", data={
        "username": username,
        "password": password,
        "confirm_password": password
    })

    # Attempt to register again with the same username
    response = flask_test_client.post("/auth/register", data={
        "username": username,
        "password": password,
        "confirm_password": password
    })
    assert response.status_code == 200 # Flask might return 200 with a flash message
    assert b"Username already exists" in response.data

@pytest.mark.timeout(10)
def test_registration_password_mismatch(setup_users, flask_test_client):
    """
    Test case for registration with mismatched passwords.
    """
    username = "e2e_mismatch_user"
    response = flask_test_client.post("/auth/register", data={
        "username": username,
        "password": "passwordA",
        "confirm_password": "passwordB"
    })
    assert response.status_code == 200 # Flask might return 200 with a flash message
    assert b"Passwords do not match" in response.data

@pytest.mark.timeout(10)
def test_registration_empty_fields(setup_users, flask_test_client):
    """
    Test case for registration with empty fields.
    """
    response = flask_test_client.post("/auth/register", data={
        "username": "",
        "password": "",
        "confirm_password": ""
    })
    assert response.status_code == 200 # Flask might return 200 with a flash message
    assert b"Username is required" in response.data
    assert b"Password is required" in response.data
    assert b"Confirm password is required" in response.data

@pytest.mark.timeout(10)
def test_successful_login(setup_users, flask_test_client):
    """
    Test case for successful user login.
    Requires a user to be pre-registered.
    """
    username = "e2e_test_user_login"
    password = "e2e_password123"

    # Ensure user is registered
    flask_test_client.post("/auth/delete_user", json={"username": username}) # Clean up
    flask_test_client.post("/auth/register", data={
        "username": username,
        "password": password,
        "confirm_password": password
    })

    response = flask_test_client.post("/auth/login", data={
        "username": username,
        "password": password
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b"Logged in successfully" in response.data

@pytest.mark.timeout(10)
def test_login_invalid_password(setup_users, flask_test_client):
    """
    Test case for login with incorrect password.
    """
    username = "e2e_invalid_pass_user"
    password = "e2e_password123"

    # Ensure user is registered
    flask_test_client.post("/auth/delete_user", json={"username": username}) # Clean up
    # Register test user
    reg_response = flask_test_client.post("/auth/register", data={
        "username": username,
        "password": password,
        "confirm_password": password
    }, follow_redirects=True)
    assert reg_response.status_code == 200

    # Test invalid password
    response = flask_test_client.post("/auth/login", data={
        "username": username,
        "password": "wrongpassword"
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b"Invalid username or password" in response.data

@pytest.mark.timeout(10)
def test_login_non_existent_username(setup_users, flask_test_client):
    """
    Test case for login with a non-existent username.
    """
    response = flask_test_client.post("/auth/login", data={
        "username": "nonexistent_e2e_user",
        "password": "anypassword"
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b"Invalid username or password" in response.data

@pytest.mark.timeout(10)
def test_login_empty_fields(setup_users, flask_test_client):
    """
    Test case for login with empty fields.
    """
    response = flask_test_client.post("/auth/login", data={
        "username": "",
        "password": ""
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b"Username is required" in response.data
    assert b"Password is required" in response.data

# Add a simple route to delete users for test cleanup
# This would typically be an admin endpoint or part of a test utility
# For demonstration, adding a placeholder here.
# In a real app, this would be secured.
# @app.route('/delete_user', methods=['POST'])
# def delete_user_for_test():
#     data = request.get_json()
#     username = data.get('username')
#     if username:
#         # Assuming you have a User model and a way to delete
#         # User.delete_user(username)
#         return jsonify({"message": f"User {username} deleted (for test cleanup)"}), 200
#     return jsonify({"message": "Username not provided"}), 400