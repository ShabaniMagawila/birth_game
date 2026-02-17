from pydantic import BaseModel, Field
from datetime import date
from typing import Optional


class UserCreate(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    date_of_birth: date
    
    class Config:
        json_schema_extra = {
            "example": {
                "first_name": "John",
                "last_name": "Doe",
                "date_of_birth": "1990-01-15"
            }
        }


class UserResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    date_of_birth: date
    age: int
    birth_day: str
    
    class Config:
        from_attributes = True
