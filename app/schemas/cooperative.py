from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import time
from datetime import datetime


class CooperativeBase(BaseModel):
    corporate_name: str
    address: str
    cnpj: str
    materials: List[str]
    phone: str
    open_time: time
    close_time: time
    latitude: Optional[float] = None
    longitude: Optional[float] = None

    class Config:
        from_attributes = True


class CooperativeCreate(CooperativeBase):
    pass


class CooperativeUpdate(BaseModel):
    corporate_name: Optional[str] = None
    address: Optional[str] = None
    cnpj: Optional[str] = None
    materials: Optional[List[str]] = None
    phone: Optional[str] = None
    open_time: Optional[time] = None
    close_time: Optional[time] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None

class Config:
        from_attributes = True


class CooperativeOut(CooperativeBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
