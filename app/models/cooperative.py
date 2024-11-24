from sqlalchemy import Column, Integer, String, DateTime, JSON, Time, Float
from sqlalchemy.sql import func
from app.core.database import Base


class Cooperative(Base):
    __tablename__ = "cooperative"

    id = Column(Integer, primary_key=True, index=True)
    corporate_name = Column(String, nullable=False)
    address = Column(String, nullable=False)
    cnpj = Column(String, nullable=False)
    materials = Column(JSON, nullable=False)
    phone = Column(String, nullable=False)
    open_time = Column(Time, nullable=False)
    close_time = Column(Time, nullable=False)
    latitude = Column(Float, nullable=True)  # Allow null values initially
    longitude = Column(Float, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
