
# API Manager

A FastAPI-based task management API with user authentication, secure task ownership, and CRUD operations. This project demonstrates how to build a small REST API using FastAPI, SQLAlchemy, JWT-based auth, and SQLite.

## Features

- User registration and login
- JWT authentication using bearer tokens
- Secure task creation, reading, updating, and deletion
- Each user can only access their own tasks
- API documentation available via Swagger UI and ReDoc
- Automated tests for authentication and access control

## Tech Stack

- FastAPI
- SQLAlchemy
- Pydantic
- SQLite
- JWT (python-jose)
- Passlib with bcrypt
- Pytest
- Docker

## Project Structure

- `main.py` - API routes and endpoint logic
- `auth.py` - JWT authentication and password hashing
- `database.py` - Database engine and session setup
- `models.py` - SQLAlchemy models for users and tasks
- `schemas.py` - Pydantic request/response schemas
- `test_main.py` - API tests
- `requirements.txt` - Python dependencies
- `Dockerfile` - Container setup for running the app

## Installation

1. Create and activate a virtual environment

```bash
python -m venv venv
source venv/bin/activate
```

On Windows PowerShell:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

If PowerShell blocks script execution, run:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
```

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the project root with the following values:

```env
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

## Running the Application

Start the server locally:

```bash
uvicorn main:app --reload
```

The API will be available at:

- http://127.0.0.1:8000
- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

## API Endpoints

### Authentication

- `POST /auth/register` - Register a new user
- `POST /auth/login` - Login and receive an access token

### Tasks

- `POST /tasks` - Create a new task
- `GET /tasks/` - List all tasks for the authenticated user
- `GET /tasks/{task_id}` - Get one task by ID
- `PUT /tasks/{task_id}` - Update a task
- `DELETE /tasks/{task_id}` - Delete a task

All task endpoints require a valid Bearer token in the `Authorization` header.

## Example Usage

### Register a User

```bash
curl -X POST "http://127.0.0.1:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"password123"}'
```

### Login

```bash
curl -X POST "http://127.0.0.1:8000/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=user@example.com&password=password123"
```

### Create a Task

```bash
curl -X POST "http://127.0.0.1:8000/tasks" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title":"Study FastAPI","description":"Build a CRUD API"}'
```

## Testing

Run the tests with:

```bash
pytest
```

## Docker

Build and run the app in Docker:

```bash
docker build -t api-manager .
docker run -p 8000:8000 api-manager
```

## Summary

This project is a practical example of building a secure and user-specific REST API with FastAPI. It covers authentication, database modeling, request validation, and API testing in a simple and beginner-friendly way.
