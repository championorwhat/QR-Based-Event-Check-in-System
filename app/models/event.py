# app/models/event.py

from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional

class EventBase(BaseModel):
    title: str
    description: str
    location: str
    date: datetime
    time: datetime

# class EventCreate(BaseModel):
#     event_name: str
#     event_date: date
#     location: str
    
class EventCreate(BaseModel):
    event_name: str
    event_date: datetime
    location: str
    organizer_id: str


class EventInDB(EventCreate):
    id: str
    organizer_id: str

