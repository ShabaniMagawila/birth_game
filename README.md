# Coolify App - Birthday Information System

A full-stack application demonstrating FastAPI backend, Flask frontend, and PostgreSQL database integration.

## Project Structure

```
Coolify_App/
├── backend/          # FastAPI backend
│   ├── main.py       # Main FastAPI application
│   ├── database.py   # Database connection
│   ├── models.py     # SQLAlchemy models
│   ├── schemas.py    # Pydantic schemas
│   ├── requirements.txt
│   ├── .env
│   └── README.md
│
├── frontend/         # Flask frontend
│   ├── app.py        # Main Flask application
│   ├── templates/    # HTML templates
│   │   ├── index.html
│   │   ├── result.html
│   │   └── users.html
│   ├── requirements.txt
│   ├── .env
│   └── README.md
│
└── database/         # PostgreSQL setup
    ├── init.sql
    ├── schema.sql
    └── README.md
```

## Features

- ✅ User registration with first name, last name, and date of birth
- ✅ Automatic age calculation
- ✅ Birth day of the week determination
- ✅ RESTful API with FastAPI
- ✅ Beautiful web interface with Flask
- ✅ PostgreSQL database
- ✅ CRUD operations for user management

## Quick Start

### 1. Database (Already Setup)

The PostgreSQL database `coolify_db` is already created and initialized on your local PostgreSQL instance.

### 2. Start the Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

Backend will be available at:
- API: http://localhost:8000
- Swagger Docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### 3. Start the Frontend

```bash
cd frontend
pip install -r requirements.txt
python app.py
```

Frontend will be available at: http://localhost:5000

## API Endpoints

### POST /users/
Create a new user
```json
{
  "first_name": "John",
  "last_name": "Doe",
  "date_of_birth": "1990-01-15"
}
```

Response:
```json
{
  "id": 1,
  "first_name": "John",
  "last_name": "Doe",
  "date_of_birth": "1990-01-15",
  "age": 36,
  "birth_day": "Monday"
}
```

### GET /users/
Get all users

### GET /users/{user_id}
Get a specific user

### DELETE /users/{user_id}
Delete a user

## Technologies Used

### Backend
- **FastAPI** - Modern, fast web framework for building APIs
- **SQLAlchemy** - SQL toolkit and ORM
- **Pydantic** - Data validation using Python type annotations
- **Uvicorn** - ASGI server

### Frontend
- **Flask** - Lightweight WSGI web application framework
- **Jinja2** - Template engine
- **Requests** - HTTP library

### Database
- **PostgreSQL** - Powerful, open-source relational database

## Environment Variables

### Backend (.env)
```
DATABASE_URL=postgresql://postgres:0000@localhost:5432/coolify_db
```

### Frontend (.env)
```
API_URL=http://localhost:8000
SECRET_KEY=your-secret-key-change-this-in-production
```

## Development

### Database Connection
The application connects to PostgreSQL using the connection string in the backend .env file. Make sure the database is running before starting the backend.

### Running Tests
```bash
# Backend
cd backend
pytest

# Frontend
cd frontend
pytest
```

## Troubleshooting

### Cannot connect to database
- Ensure PostgreSQL service is running on your machine
- Verify connection details in backend/.env match your local PostgreSQL credentials
- Test connection: `$env:PGPASSWORD='0000'; psql -U postgres -h localhost -d coolify_db`

### Backend API not responding
- Check if uvicorn is running on port 8000
- Look for errors in terminal output
- Verify database connection

### Frontend cannot connect to backend
- Ensure backend is running on port 8000
- Check API_URL in frontend/.env
- Verify CORS settings in backend

## License

MIT License - feel free to use this project for learning and demonstration purposes.

## Author

Created as a demonstration project for the Coolify App.
