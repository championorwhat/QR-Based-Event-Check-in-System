# app/models.py

from pydantic import BaseModel

# Pydantic models for user input
class UserCreate(BaseModel):
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class User(BaseModel):
    id: str  # This should be a string.
    username: str
    email: str
    # Other fields here as needed

    class Config:
        json_encoders = {
            ObjectId: str  # To handle ObjectId serialization.
        }