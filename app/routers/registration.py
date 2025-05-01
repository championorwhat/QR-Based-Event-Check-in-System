# from fastapi import APIRouter, HTTPException, Depends
# from app.models.registration import RegistrationCreate
# from app.database import registration_collection
# from app.auth import get_current_user
# from app.models.user import User
# from bson import ObjectId
# from datetime import datetime
# from app.database import event_collection
# import qrcode
# from io import BytesIO
# from fastapi.responses import StreamingResponse
# import base64
# from fastapi.exception_handlers import request_validation_exception_handler
# from bson.errors import InvalidId
# from pydantic import ValidationError
# from app.utils.email import send_email_with_qr_code  # Import email sending function


# router = APIRouter(
#     prefix="/registration",
#     tags=["Registrations"]
# )

# # @router.post("/register")
# # async def register_for_event(
# #     registration: RegistrationCreate, 
# #     current_user: User = Depends(get_current_user)
# # ):
# #     # Check if the event exists
# #     event = await event_collection.find_one({"_id": ObjectId(registration.event_id)})
# #     if not event:
# #         raise HTTPException(status_code=404, detail="Event not found")
    
# #     # Register the user for the event
# #     registration_data = {
# #         "event_id": registration.event_id,
# #         "user_id": str(current_user.id),
# #         "registration_date": datetime.utcnow()
# #     }
    
# #     result = await registration_collection.insert_one(registration_data)
    
# #     if result.inserted_id:
# #         registration_id = str(result.inserted_id)
# #         # Generate QR Code for registration
# #         qr_code_image = generate_qr_code_base64(registration_id)
# #         return {"message": "Registration successful", "registration_id": registration_id, "qr_code_image": qr_code_image}
# #     else:
# #         raise HTTPException(status_code=500, detail="Failed to register")

# # @router.post("/register")
# # async def register_for_event(
# #     registration: RegistrationCreate, 
# #     current_user: User = Depends(get_current_user)
# # ):
# #     print("Registering user:", current_user.id, "to event:", registration.event_id)

# #     event = await event_collection.find_one({"_id": ObjectId(registration.event_id)})
# #     if not event:
# #         raise HTTPException(status_code=404, detail="Event not found")
    
# #     registration_data = {
# #         "event_id": registration.event_id,
# #         "user_id": str(current_user.id),
# #         "registration_date": datetime.utcnow()
# #     }
    
# #     result = await registration_collection.insert_one(registration_data)
    
# #     if result.inserted_id:
# #         registration_id = str(result.inserted_id)
        
# #         # ✅ Generate QR Code as base64 string
# #         qr_code_base64 = generate_qr_code_base64(registration_id)
        
# #         return {
# #             "message": "Registration successful",
# #             "registration_id": registration_id,
# #             "qr_code_base64": qr_code_base64  # ✅ JSON-safe string
# #         }
# #     else:
# #         raise HTTPException(status_code=500, detail="Failed to register")



# @router.post("/register")
# async def register_for_event(
#     registration: RegistrationCreate,
#     current_user: User = Depends(get_current_user)
# ):
#     try:
#         print("DEBUG: User ID:", current_user.id)
#         print("DEBUG: Event ID:", registration.event_id)

#         try:
#             event_obj_id = ObjectId(registration.event_id)
#         except InvalidId as e:
#             raise HTTPException(status_code=400, detail="Invalid event ID format")

#         event = await event_collection.find_one({"_id": event_obj_id})
#         if not event:
#             raise HTTPException(status_code=404, detail="Event not found")

#         registration_data = {
#             "event_id": registration.event_id,
#             "user_id": str(current_user.id),
#             "registration_date": datetime.utcnow()
#         }

#         result = await registration_collection.insert_one(registration_data)

#         if result.inserted_id:
#             registration_id = str(result.inserted_id)
#             qr_code_base64 = generate_qr_code_base64(registration_id)
#             send_email_with_qr_code("pg7931@srmist.edu.in", qr_code_base64, registration_id)

#             return {
#                 "message": "Registration successful",
#                 "registration_id": registration_id,
#                 "qr_code_base64": qr_code_base64
#             }
#         else:
#             raise HTTPException(status_code=500, detail="Failed to register")

#     except ValidationError as e:
#         print("Validation Error:", e.json())
#         raise HTTPException(status_code=422, detail=e.errors())
    
# @router.get("/qr/{registration_id}")
# async def get_qr_code(registration_id: str):
#     """
#     Endpoint to fetch the QR code image for the registration using registration_id.
#     """
#     # Generate the QR code image from the registration ID
#     qr_code_base64 = generate_qr_code_base64(registration_id)

#     # Convert the base64 string to a binary image and return it as a PNG image
#     img_data = base64.b64decode(qr_code_base64)
#     return StreamingResponse(BytesIO(img_data), media_type="image/png")


# def generate_qr_code_base64(data: str) -> str:
#     img = qrcode.make(data)
#     buf = BytesIO()
#     img.save(buf, format="PNG")
#     buf.seek(0)
#     img_base64 = base64.b64encode(buf.read()).decode("utf-8")
#     return img_base64














from fastapi import APIRouter, HTTPException, Depends
from app.models.registration import RegistrationCreate
from app.database import registration_collection
from app.auth import get_current_user
from app.models.user import User
from bson import ObjectId
from datetime import datetime
from app.database import event_collection
import qrcode
from io import BytesIO
from fastapi.responses import StreamingResponse
import base64
from fastapi.exception_handlers import request_validation_exception_handler
from bson.errors import InvalidId
from pydantic import ValidationError
from app.utils.email import send_email_with_qr_code  # Import email sending function


router = APIRouter(
    prefix="/registration",
    tags=["Registrations"]
)

@router.post("/register")
async def register_for_event(
    registration: RegistrationCreate,
    current_user: User = Depends(get_current_user)
):
    try:
        # Debug prints
        print("DEBUG: User ID:", current_user.id)
        print("DEBUG: Event ID:", registration.event_id)

        try:
            event_obj_id = ObjectId(registration.event_id)
        except InvalidId as e:
            raise HTTPException(status_code=400, detail="Invalid event ID format")

        event = await event_collection.find_one({"_id": event_obj_id})
        if not event:
            raise HTTPException(status_code=404, detail="Event not found")

        registration_data = {
            "event_id": registration.event_id,
            "user_id": str(current_user.id),
            "registration_date": datetime.utcnow()
        }

        result = await registration_collection.insert_one(registration_data)

        if result.inserted_id:
            registration_id = str(result.inserted_id)
            qr_code_base64 = generate_qr_code_base64(registration_id)

            # Send email with QR code attached
            try:
                send_email_with_qr_code("example@test.com", qr_code_base64, registration_id)
            except Exception as e:
                print(f"Error sending email: {e}")
                raise HTTPException(status_code=500, detail="Failed to send registration email")

            return {
                "message": "Registration successful",
                "registration_id": registration_id,
                "qr_code_base64": qr_code_base64
            }
        else:
            raise HTTPException(status_code=500, detail="Failed to register")

    except ValidationError as e:
        print("Validation Error:", e.json())
        raise HTTPException(status_code=422, detail=e.errors())

@router.get("/qr/{registration_id}")
async def get_qr_code(registration_id: str):
    """
    Endpoint to fetch the QR code image for the registration using registration_id.
    """
    # Generate the QR code image from the registration ID
    qr_code_base64 = generate_qr_code_base64(registration_id)

    # Convert the base64 string to a binary image and return it as a PNG image
    img_data = base64.b64decode(qr_code_base64)
    return StreamingResponse(BytesIO(img_data), media_type="image/png")


def generate_qr_code_base64(data: str) -> str:
    img = qrcode.make(data)
    buf = BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    img_base64 = base64.b64encode(buf.read()).decode("utf-8")
    return img_base64
