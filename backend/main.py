from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import datetime, date
from typing import List
import calendar

from database import get_db, engine
from models import Base, User
from schemas import UserCreate, UserResponse

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="User Birthday API")

# CORS middleware to allow frontend to communicate
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def calculate_age(birth_date: date) -> int:
    """Calculate age from birth date"""
    today = date.today()
    age = today.year - birth_date.year
    if (today.month, today.day) < (birth_date.month, birth_date.day):
        age -= 1
    return age


def get_birth_day(birth_date: date) -> str:
    """Get the day of the week for birth date"""
    day_name = calendar.day_name[birth_date.weekday()]
    return day_name


@app.get("/")
def read_root():
    return {"message": "Welcome to User Birthday API"}


@app.post("/users/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """Create a new user and return their details with calculated age and birth day"""
    
    # Create new user
    db_user = User(
        first_name=user.first_name,
        last_name=user.last_name,
        date_of_birth=user.date_of_birth
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    # Calculate additional information
    age = calculate_age(db_user.date_of_birth)
    birth_day = get_birth_day(db_user.date_of_birth)
    
    return UserResponse(
        id=db_user.id,
        first_name=db_user.first_name,
        last_name=db_user.last_name,
        date_of_birth=db_user.date_of_birth,
        age=age,
        birth_day=birth_day
    )


@app.get("/users/", response_model=List[UserResponse])
def get_all_users(db: Session = Depends(get_db)):
    """Get all users with their calculated age and birth day"""
    users = db.query(User).all()
    
    result = []
    for user in users:
        age = calculate_age(user.date_of_birth)
        birth_day = get_birth_day(user.date_of_birth)
        
        result.append(UserResponse(
            id=user.id,
            first_name=user.first_name,
            last_name=user.last_name,
            date_of_birth=user.date_of_birth,
            age=age,
            birth_day=birth_day
        ))
    
    return result


@app.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    """Get a specific user by ID"""
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    age = calculate_age(user.date_of_birth)
    birth_day = get_birth_day(user.date_of_birth)
    
    return UserResponse(
        id=user.id,
        first_name=user.first_name,
        last_name=user.last_name,
        date_of_birth=user.date_of_birth,
        age=age,
        birth_day=birth_day
    )


@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    """Delete a user by ID"""
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    db.delete(user)
    db.commit()
    
    return {"message": "User deleted successfully"}
