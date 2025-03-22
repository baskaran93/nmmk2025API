import asyncio
import datetime
import os
from fastapi import HTTPException, Request
from dotenv import load_dotenv
import jwt
from functools import wraps

load_dotenv()

SECRECT_KEY=os.getenv("SECRECT_KEY")
ALGORITHM = "HS256"

def create_access_token(data:dict, expires_delta:datetime.timedelta):
    to_encode = data.copy()
    expires = datetime.datetime.utcnow()+expires_delta
    to_encode.update({"exp": expires})
    encoded_jwt = jwt.encode(to_encode, SECRECT_KEY, ALGORITHM)
    return encoded_jwt

def verify_access_token(token):
    try:
        payload = jwt.decode(token, SECRECT_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")


def get_token_from_header(request: Request):
    """Extracts and verifies JWT token from Authorization header"""
    auth_header = request.headers.get("Authorization")

    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Authorization header missing or invalid")
    token = auth_header.split(" ")[1]
    return verify_access_token(token)

# Custom decorator to use in FastAPI routes
def require_auth(request: Request):
    """Extracts JWT token from Authorization header and verifies it"""
    auth_header = request.headers.get("Authorization")

    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Authorization header missing or invalid")

    token = auth_header.split(" ")[1]
    return verify_access_token(token)  # Returns user data if token is valid