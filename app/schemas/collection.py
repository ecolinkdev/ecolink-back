from pydantic import BaseModel
from datetime import datetime
from typing import List, Dict, Union
from app.models.collection import CollectionStatus


class CollectionBase(BaseModel):
    date: datetime
    time: str
    address: str
    materials: List[Dict[str, Union[str, int]]]  # Melhor para suportar múltiplos tipos
    status: CollectionStatus = CollectionStatus.pending


class CollectionCreate(CollectionBase):
    pass


class CollectionUpdate(BaseModel):
    status: CollectionStatus


class Collection(CollectionBase):
    id: int
    user_id: int
    created_at: datetime
    updated_t: Union[datetime, None]  # Forma explícita de tratar None

    class Config:
        from_attributes = True  # Certifica que o modelo será compatível com SQLAlchemy
