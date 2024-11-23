from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from app.models.user import UserType

class UserBase(BaseModel):
    email: EmailStr
    name: str
    type: UserType
    address: str
    phone: str
    document: str

class UserCreate(UserBase):
    password: str

class UserUpdate(UserBase):
    password: Optional[str] = None

class UserInDBBase(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class User(UserInDBBase):
    pass