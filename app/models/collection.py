from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum, JSON, Float
from sqlalchemy.sql import func
from app.core.database import Base
import enum

class CollectionStatus(str, enum.Enum):
    pending = "pending"
    collected = "collected"

class Collection(Base):
    __tablename__ = "collections"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    date = Column(DateTime, nullable=False)
    time = Column(String, nullable=False)
    address = Column(String, nullable=False)
    materials = Column(JSON, nullable=False)  # Store materials as JSON
    status = Column(Enum(CollectionStatus), default=CollectionStatus.pending)
    latitude = Column(Float, nullable=True)  # Allow null values initially
    longitude = Column(Float, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_t = Column(DateTime(timezone=True), onupdate=func.now())