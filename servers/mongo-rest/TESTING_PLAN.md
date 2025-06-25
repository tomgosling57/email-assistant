# Testing Suite Plan for Mongo-REST API

## 1. Introduction and Goals

The goal is to establish a robust testing suite for the Mongo-REST API to ensure its reliability, maintainability, and correctness. This plan will cover End-to-End (E2E), Integration, and Unit testing strategies.

## 2. Chosen Framework: Pytest

`pytest` will be the primary testing framework due to its simplicity, extensibility, and wide adoption in the Python community.

## 3. Testing Strategies

### 3.1. End-to-End (E2E) Testing

*   **Purpose**: Verify the entire system flow, from API request to database interaction and response. These tests will simulate real user interactions.
*   **Tools**: `pytest`, `httpx` (for asynchronous HTTP requests, better suited for FastAPI), `testcontainers[mongodb]` (for spinning up a temporary MongoDB instance for testing).
*   **Scope**:
    *   Verify all CRUD operations (`POST`, `GET`, `PUT`, `DELETE`) for the `/users` endpoint.
    *   Test edge cases:
        *   Retrieving a non-existent user.
        *   Updating a non-existent user.
        *   Deleting a non-existent user.
        *   Invalid `user_id` format.
        *   Invalid input data for `POST` and `PUT` requests (e.g., missing required fields, incorrect data types).
*   **Approach**:
    1.  **Setup**: Use `testcontainers` to start a fresh MongoDB instance before each test run (or test session). This ensures test isolation and repeatable results. Alternatively, for efficiency, connect to an existing MongoDB instance and use a dedicated test database name, dropping the database before each test run.
    2.  **API Client**: Use `httpx.AsyncClient` to make requests to the FastAPI application.
    3.  **Fixtures**: Create `pytest` fixtures for:
        *   Providing a test client for the FastAPI app.
        *   Setting up and tearing down the test MongoDB database (e.g., clearing collections before each test).
        *   Creating and cleaning up test data (e.g., a test user).
*   **File Location**: `servers/mongo-rest/tests/e2e/test_users_e2e.py`

### 3.2. Integration Testing

*   **Purpose**: Verify the interaction between different components, primarily the API logic (`routes.py`) and the database layer (`database.py`). These tests will ensure that the application correctly interacts with MongoDB.
*   **Tools**: `pytest`, `pymongo` (direct interaction with MongoDB), `mongomock` (optional, for mocking MongoDB if a real instance is not desired for specific tests, though `testcontainers` or a dedicated test database is preferred for true integration).
*   **Scope**:
    *   Test `database.py` functions directly to ensure they correctly interact with the MongoDB client and collections.
    *   Test `routes.py` functions by mocking the `get_users_collection` to return a mock collection, but still verifying the logic within the route functions. This is a hybrid approach, leaning towards unit testing the route logic while ensuring the database interaction *pattern* is correct.
*   **Approach**:
    1.  **Database Interaction**: Directly test `get_users_collection` and other database helper functions.
    2.  **Mocking**: Use `unittest.mock.patch` or `pytest-mock` to mock the `get_users_collection` call within `routes.py` to control the database responses for specific scenarios without hitting a real database.
*   **File Location**: `servers/mongo-rest/tests/integration/test_database_integration.py` (for `database.py` functions) and `servers/mongo-rest/tests/integration/test_routes_integration.py` (for `routes.py` with mocked database).

### 3.3. Unit Testing

*   **Purpose**: Test individual functions, methods, or classes in isolation, mocking all external dependencies.
*   **Tools**: `pytest`, `unittest.mock` or `pytest-mock`.
*   **Scope**:
    *   **`models.py`**:
        *   Test `PyObjectId` validation (valid and invalid ObjectIds).
        *   Test `User` and `UserCreate` model validation (e.g., required fields, data types).
    *   **`routes.py`**:
        *   Test the logic within each route function, mocking the `get_users_collection` and its methods (`find`, `find_one`, `insert_one`, `update_one`, `delete_one`).
        *   Verify `HTTPException` raising for invalid inputs or not found scenarios.
    *   **`database.py`**:
        *   Test `get_db` and `get_users_collection` to ensure they return the correct objects (mocking `MongoClient`).
*   **Approach**:
    1.  **Isolation**: Each test should focus on a single unit of code.
    2.  **Mocking**: Mock all external dependencies to ensure the test only verifies the logic of the unit under test.
*   **File Location**:
    *   `servers/mongo-rest/tests/unit/test_models.py`
    *   `servers/mongo-rest/tests/unit/test_routes.py`
    *   `servers/mongo-rest/tests/unit/test_database.py`

## 4. Test Directory Structure

```
servers/mongo-rest/
├── src/
│   ├── __init__.py
│   ├── config.py
│   ├── database.py
│   ├── main.py
│   ├── models.py
│   └── routes.py
├── tests/
│   ├── __init__.py
│   ├── e2e/
│   │   ├── __init__.py
│   │   └── test_users_e2e.py
│   ├── integration/
│   │   ├── __init__.py
│   │   ├── test_database_integration.py
│   │   └── test_routes_integration.py
│   └── unit/
│       ├── __init__.py
│       ├── test_models.py
│       ├── test_routes.py
│       └── test_database.py
├── test_api.py (can be removed or refactored into e2e tests)
└── ...
```

## 5. Dependencies

Add the following to `servers/mongo-rest/requirements.txt`:
*   `pytest`
*   `httpx`
*   `pytest-mock` (for mocking)
*   `testcontainers[mongodb]` (for E2E testing with a real MongoDB instance, if chosen)

## 6. Running Tests

*   To run all tests: `pytest` from the `servers/mongo-rest/` directory.
*   To run specific tests: `pytest tests/e2e/test_users_e2e.py`

## 7. Continuous Integration (CI)

Integrate the testing suite into a CI pipeline (e.g., GitHub Actions, GitLab CI) to automatically run tests on every push or pull request, ensuring code quality and preventing regressions.

## 8. Next Steps

Upon approval of this plan, I will proceed with:
1.  Creating the `tests` directory structure.
2.  Updating `requirements.txt`.
3.  Implementing the test cases as outlined.