# app/schemas/user.py

from app.models.user import UserInDB
from app.database import get_db
from bson import ObjectId

async def create_user(user: UserInDB):
    db = get_db()
    user_dict = user.dict()
    result = await db.users.insert_one(user_dict)
    return str(result.inserted_id)

async def get_user_by_email(email: str):
    db = get_db()
    user = await db.users.find_one({"email": email})
    return user
