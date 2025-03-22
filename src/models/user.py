from sqlalchemy.orm import declarative_base
from pydantic import BaseModel, EmailStr
from sqlalchemy import Column, Integer, String, DateTime, Boolean
import datetime
from typing import Optional

BASE = declarative_base()

class User(BASE):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    phone = Column(String, unique=True, index=True, nullable=False)
    address = Column(String, unique=True, index=True, nullable=True)
    pincode = Column(String, unique=True, index=True, nullable=True)
    registration_time = Column(DateTime, default=datetime.datetime.utcnow, nullable=True)
    checked_in_time = Column(DateTime, nullable=True)
    is_checked_in = Column(Boolean, default=False)
    food_checked_in_time = Column(DateTime, nullable=True)
    is_food_checked_in = Column(Boolean, default=False)


class UserCreate(BaseModel):
    name: str
    email: Optional[EmailStr] = None
    phone: str
    address: Optional[str] = None
    pincode: Optional[int] = 625001


class UserCheckIn(BaseModel):
    id: Optional[str] = None
    phone: Optional[str] = None


class GetUserId(BaseModel):
    phone: str

class VerifyUserId(BaseModel):
    id: str

class UserRegister(BaseModel):
    username: str
    password_hash: str


class UserLogin(BASE):
    __tablename__ = "user_login"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    password_reset_time = Column(DateTime, nullable=True)