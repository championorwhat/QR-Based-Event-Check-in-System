# app/models/user.py

from pydantic import BaseModel,EmailStr
from typing import Optional

class UserRequest(BaseModel):
    username: str
    email: EmailStr
    password: str

# class UserBase(BaseModel):
#     name: str
#     email: str
#     student_id: str

# class UserCreate(UserBase):
#     password: str

# class UserInDB(UserBase):
#     password_hash: str
#     role: str
    
class UserLogin(BaseModel):
    username: str
    password: str


class User(BaseModel):
    id: Optional[str]  # id will come from MongoDB (_id), optional because during login it may not exist
    username: str
    email: EmailStr
