# app/routers/user.py

from fastapi import APIRouter, HTTPException, Depends
from app.auth import create_access_token, verify_password, get_password_hash,verify_token
from app.database import get_user_collection
from app.models.user import UserRequest, UserLogin
from motor.motor_asyncio import AsyncIOMotorCollection
from bson import ObjectId
import qrcode
from pathlib import Path
from app.utils.qr import generate_qr_code

router = APIRouter()

# 
# User registration route
@router.post("/register")
async def register_user(user: UserRequest, db: AsyncIOMotorCollection = Depends(get_user_collection)):
    # Check if the user already exists
    existing_user = await db.find_one({"username": user.username})
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")
    
    hashed_password = get_password_hash(user.password)
    new_user = {
        "username": user.username,
        "email": user.email,
        "password": hashed_password
    }
    
    # Insert the new user into the database
    result = await db.insert_one(new_user)
    return {"message": "User registered successfully", "user_id": str(result.inserted_id)}

# @router.post("/login")
# async def login_user(user: UserLogin, db: AsyncIOMotorCollection = Depends(get_user_collection)):
#     # Check if user exists
#     db_user = await db.find_one({"username": user.username})
    
#     if not db_user or not verify_password(user.password, db_user["password"]):
#         raise HTTPException(status_code=401, detail="Invalid credentials")
    
#     # Create a JWT token
#     token = create_access_token(data={"sub": user.username})
    
#     return {"access_token": token, "token_type": "bearer"}

@router.post("/login")
async def login_user(user: UserLogin, db: AsyncIOMotorCollection = Depends(get_user_collection)):
    # Check if user exists
    db_user = await db.find_one({"username": user.username})
    
    if not db_user or not verify_password(user.password, db_user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Create a JWT token with user _id
    token = create_access_token(data={"sub": str(db_user["_id"])})
    access_token = create_access_token(data={"sub": user.username})

    return {"access_token": token, "token_type": "bearer"}


# Secured route to test token
@router.get("/me")
async def read_users_me(db: AsyncIOMotorCollection = Depends(get_user_collection), current_user: str = Depends(verify_token)):
    user = await db.find_one({"_id": ObjectId(current_user)})
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    user["_id"] = str(user["_id"])
    user_data = {key: value for key, value in user.items() if key != "password"}
    return user_data



@router.get("/{username}")
async def get_user_details(
    username: str,
    db: AsyncIOMotorCollection = Depends(get_user_collection),
    current_user_id: str = Depends(verify_token)
):
    user = await db.find_one({"_id": ObjectId(current_user_id)})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if username != user["username"]:
        raise HTTPException(status_code=403, detail="Not authorized")

    user["_id"] = str(user["_id"])
    user_data = {k: v for k, v in user.items() if k != "password"}
    return user_data

    
    return user_data

@router.put("/{username}/update")
async def update_user_details(
    username: str,
    user: UserRequest,
    db: AsyncIOMotorCollection = Depends(get_user_collection),
    current_user: str = Depends(verify_token)  # This is user_id
):
    current_user_data = await db.find_one({"_id": ObjectId(current_user)})
    if not current_user_data or current_user_data["username"] != username:
        raise HTTPException(status_code=403, detail="Not authorized")

    updated_data = {
        "email": user.email,
        "password": get_password_hash(user.password)
    }

    result = await db.update_one({"username": username}, {"$set": updated_data})
    if result.modified_count == 0:
        raise HTTPException(status_code=400, detail="No changes made")

    return {"message": "User details updated successfully"}

@router.delete("/{username}/delete")
async def delete_user(username: str, db: AsyncIOMotorCollection = Depends(get_user_collection), current_user: str = Depends(verify_token)):
    # Ensure that the current user is the one requesting deletion
    if username != current_user:
        raise HTTPException(status_code=403, detail="Not authorized to delete this user's details")
    
    result = await db.delete_one({"username": username})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {"message": "User deleted successfully"}


# def generate_qr_for_user(user_id: str) -> str:
#     qr = qrcode.QRCode(version=1, box_size=10, border=4)
#     qr.add_data(user_id)
#     qr.make(fit=True)

#     img = qr.make_image(fill="black", back_color="white")
#     output_path = Path("qr_codes")
#     output_path.mkdir(parents=True, exist_ok=True)
#     img_path = output_path / f"user_{user_id}.png"
#     img.save(img_path)

#     return str(img_path)

# from app.utils.qr import generate_qr_for_checkin  # Assuming it's in utils/qr.py

@router.get("/generate-checkin-qr")
async def generate_checkin_qr(
    event_id: str,
    db: AsyncIOMotorCollection = Depends(get_user_collection),
    current_user: str = Depends(verify_token)
):
    user = await db.find_one({"_id": ObjectId(current_user)})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    qr_base64 = generate_qr_for_checkin(user_id=str(user["_id"]), event_id=event_id)
    
    return {
        "message": f"QR code generated for event {event_id}",
        "qr_code_base64": qr_base64
    }

@router.get("/checkin")
async def check_in_user(user_id: str, event_id: str, db: AsyncIOMotorCollection = Depends(get_user_collection)):
    user = await db.find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Add a basic check-in log (you can extend this with timestamp etc.)
    checkin_info = {
        "event_id": event_id,
        "user_id": user_id
    }

    # Save to check-ins (assumes you have a separate collection for check-ins)
    checkin_collection = db.database["checkins"]  # reuse same db connection
    await checkin_collection.insert_one(checkin_info)

    return {
        "message": f"✅ User {user['username']} checked in for event {event_id}"
    }
