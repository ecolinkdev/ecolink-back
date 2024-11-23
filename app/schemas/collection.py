from pydantic import BaseModel
from datetime import datetime
from typing import List, Dict
from app.models.collection import CollectionStatus

class CollectionBase(BaseModel):
    date: datetime
    time: str
    address: str
    materials: List[Dict[str, str | int]]
    status: CollectionStatus = CollectionStatus.pending

class CollectionCreate(CollectionBase):
    pass

class CollectionUpdate(BaseModel):
    status: CollectionStatus

class Collection(CollectionBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime | None

    class Config:
        from_attributes = True