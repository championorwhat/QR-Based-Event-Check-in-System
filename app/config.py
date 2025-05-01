# app/config.py

# import os
# from dotenv import load_dotenv

# load_dotenv()  # Loads variables from .env file

# MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")  # Default to local MongoDB
# JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your_secret_key")


# app/config.py
import os
from dotenv import load_dotenv

load_dotenv()  # Loads variables from .env file

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your_secret_key")
print("JWT_SECRET_KEY:", JWT_SECRET_KEY)  # Check if it's loading correctly
