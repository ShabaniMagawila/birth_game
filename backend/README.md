# FastAPI Backend

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Make sure PostgreSQL is running with coolify_db database created

3. Run the application:
```bash
uvicorn main:app --reload --port 8000
```

## API Endpoints

- `POST /users/` - Create a new user
- `GET /users/` - Get all users
- `GET /users/{user_id}` - Get a specific user
- `DELETE /users/{user_id}` - Delete a user

## API Documentation

Once running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
