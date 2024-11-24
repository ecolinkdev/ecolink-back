from pydantic import BaseModel
from datetime import datetime
from typing import List, Dict, Union, Optional
from app.models.collection import CollectionStatus


class CollectionBase(BaseModel):
    date: datetime
    time: str
    address: str
    materials: List[Dict[str, Union[str, int]]]  # Suporta combinações de tipos
    status: CollectionStatus = CollectionStatus.pending
    latitude: Optional[float] = None
    longitude: Optional[float] = None


class CollectionCreate(CollectionBase):
    pass


class CollectionUpdate(BaseModel):
    status: CollectionStatus
    latitude: Optional[float] = None
    longitude: Optional[float] = None


class Collection(CollectionBase):
    id: int
    user_id: int
    created_at: datetime
    updated_t: Union[datetime, None]  # Forma explícita de tratar None
    latitude: Optional[float] = None
    longitude: Optional[float] = None

    class Config:
        from_attributes = True  # Compatibilidade com SQLAlchemy
