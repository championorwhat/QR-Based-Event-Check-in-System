# app/database.py

import motor.motor_asyncio
from fastapi import HTTPException

MONGO_URI = "mongodb://localhost:27017"

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)

db = client.get_database("my_database")  # your database

# MongoDB collection for users
user_collection = db.get_collection("users")

async def ping_db():
    try:
        await client.admin.command('ping')
        print("✅ MongoDB connected successfully!")
    except Exception as e:
        print("❌ MongoDB connection failed:", e)

# Dependency to get the user collection
async def get_user_collection():
    return user_collection

event_collection = db.get_collection("events")

registration_collection = db["registrations"]  # Registration collection
event_collection = db["events"]  # Event collection

async def get_event_collection():
    return event_collection