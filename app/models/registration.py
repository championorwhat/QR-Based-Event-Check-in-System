# app/models/registration.py

from pydantic import BaseModel
from datetime import datetime
from bson import ObjectId

class Registration(BaseModel):
    user_id: str
    event_id: str
    qr_code: str
    checked_in: bool = False


class RegistrationCreate(BaseModel):
    event_id: str
    # user_id: str

    class Config:
        orm_mode = True

class RegistrationInDB(RegistrationCreate):
    id: str
    registration_date: datetime
