from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from app.models.user import User, UserRequest
from app.database import user_collection
from app.config import JWT_SECRET_KEY
import logging
from bson import ObjectId

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/login")  # Make sure your login URL matches this

# Constants
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


# Create JWT Access Token
def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# Password Verification
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


# Password Hashing
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


# Verify JWT Token and return Username
def verify_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        print(f"Decoded Payload: {payload}")  # Log to verify token contents
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        return username
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid credentials")


# Get Current Logged-in User

async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")  # Get user ID from token
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")

        # Fetch user from DB using _id
        user_data = await user_collection.find_one({"_id": ObjectId(user_id)})
        if user_data is None:
            raise HTTPException(status_code=404, detail="User not found")

        # Convert _id to id and ensure it is a string
        user_data["id"] = str(user_data["_id"])  # Add this line to convert ObjectId to string
        del user_data["_id"]  # Remove the original _id field
        
        return User(**user_data)

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    except Exception as e:
        logging.error(f"[get_current_user] Error occurred: {e}")
        raise HTTPException(status_code=422, detail="Invalid data format")


    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    except Exception as e:
        logging.error(f"[get_current_user] Error occurred: {e}")
        raise HTTPException(status_code=422, detail="Invalid data format")


