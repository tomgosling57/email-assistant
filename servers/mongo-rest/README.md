# Mongo-REST API

A FastAPI service providing REST endpoints for MongoDB operations.

## Setup

1. Clone the repository
2. Navigate to `servers/mongo-rest/`
3. Run:
   ```bash
   docker-compose up -d
   ```

## Running

The API will be available at `http://localhost:8000`

## API Endpoints

- `GET /users` - List all users
- `GET /users/{id}` - Get single user
- `POST /users` - Create new user
- `PUT /users/{id}` - Update user
- `DELETE /users/{id}` - Delete user