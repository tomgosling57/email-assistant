import requests
import json

BASE_URL = "http://localhost:8000"

def test_create_user():
    print("Testing POST /users")
    user_data = {
        "name": "Test User",
        "email": "test@example.com"
    }
    response = requests.post(f"{BASE_URL}/users", json=user_data)
    print(f"Response Status Code: {response.status_code}")
    print(f"Response Body: {response.text}")
    assert response.status_code == 201, f"Expected status code 201, got {response.status_code}. Response: {response.text}"
    user = response.json()
    print("Created user:", user)
    return user["_id"]

def test_get_user(user_id):
    print(f"Testing GET /users/{user_id}")
    response = requests.get(f"{BASE_URL}/users/{user_id}")
    print(f"Response Status Code: {response.status_code}")
    print(f"Response Body: {response.text}")
    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}. Response: {response.text}"
    print("Retrieved user:", response.json())

def test_list_users():
    print("Testing GET /users")
    response = requests.get(f"{BASE_URL}/users")
    print(f"Response Status Code: {response.status_code}")
    print(f"Response Body: {response.text}")
    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}. Response: {response.text}"
    print(f"Found {len(response.json())} users")

def test_update_user(user_id):
    print(f"Testing PUT /users/{user_id}")
    update_data = {
        "name": "Updated User",
        "email": "updated@example.com"
    }
    response = requests.put(f"{BASE_URL}/users/{user_id}", json=update_data)
    print(f"Response Status Code: {response.status_code}")
    print(f"Response Body: {response.text}")
    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}. Response: {response.text}"
    print("Updated user:", response.json())

def test_delete_user(user_id):
    print(f"Testing DELETE /users/{user_id}")
    response = requests.delete(f"{BASE_URL}/users/{user_id}")
    print(f"Response Status Code: {response.status_code}")
    print(f"Response Body: {response.text}")
    assert response.status_code == 204, f"Expected status code 204, got {response.status_code}. Response: {response.text}"
    print("User deleted successfully")

if __name__ == "__main__":
    print("Starting API tests...")
    try:
        # Run tests in sequence
        user_id = test_create_user()
        test_get_user(user_id)
        test_list_users()
        test_update_user(user_id)
        test_delete_user(user_id)
        print("All tests passed successfully!")
    except Exception as e:
        print(f"Test failed: {str(e)}")