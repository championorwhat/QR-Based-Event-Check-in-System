from fastapi import APIRouter, Depends, HTTPException
from app.models.event import EventCreate
from app.models.user import User
from app.database import get_event_collection, event_collection
from app.auth import get_current_user
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorCollection

router = APIRouter(
    prefix="/event",
    tags=["Events"]
)

# @router.post("/create")
# async def create_event(event: EventCreate, current_user: User = Depends(get_current_user)):
#     event_data = {
#         "event_name": event.event_name,
#         "event_date": event.event_date.isoformat(),  # store as ISO string
#         "location": event.location,
#         "organizer_id": str(current_user.id)  # Store the organizer (user who is logged in)
#     }
#     event_data["organizer_id"] = ObjectId(event.organizer_id)
#     result = await event_collection.insert_one(event_data)
#     if result.inserted_id:
#         # Fetch the inserted event to return full details
#         created_event = await event_collection.find_one({"_id": result.inserted_id})
#         # Convert ObjectId to string for returning in JSON
#         created_event["_id"] = str(created_event["_id"])
#         return {"message": "Event created successfully", "event": created_event}
#     else:
#         raise HTTPException(status_code=500, detail="Failed to create event")

@router.post("/events")
async def create_event(event: EventCreate):
    new_event = event.dict()
    result = await event_collection.insert_one(new_event)
    new_event["_id"] = str(result.inserted_id)  # Convert ObjectId to string
    return new_event

@router.get("/events")
async def list_events():
    events = []
    async for event in event_collection.find():
        event["_id"] = str(event["_id"])  # Convert each ObjectId
        events.append(event)
    return events
