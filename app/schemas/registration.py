# app/schemas/registration.py

from app.models.registration import Registration
from app.database import get_db

async def register_user_for_event(registration: Registration):
    db = get_db()
    registration_dict = registration.dict()
    result = await db.registrations.insert_one(registration_dict)
    return str(result.inserted_id)


