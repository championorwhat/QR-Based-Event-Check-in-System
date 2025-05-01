# app/schemas/event.py

from app.models.event import EventInDB
from app.database import get_db
from bson import ObjectId

async def create_event(event: EventInDB):
    db = get_db()
    event_dict = event.dict()
    result = await db.events.insert_one(event_dict)
    return str(result.inserted_id)

async def get_event_by_id(event_id: str):
    db = get_db()
    event = await db.events.find_one({"_id": ObjectId(event_id)})
    return event
