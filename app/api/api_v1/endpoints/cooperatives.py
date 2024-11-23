from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.cooperative import CooperativeCreate, CooperativeOut as CooperativeSchema
from app.models.cooperative import Cooperative

router = APIRouter()


@router.get("/", response_model=List[CooperativeSchema])
def list_cooperatives(db: Session = Depends(get_db), skip: int = 0,
                      limit: int = 100):
    """
    Rota para listar todas as cooperativas.
    """
    cooperatives = db.query(Cooperative).offset(skip).limit(limit).all()
    return cooperatives


@router.post("/", response_model=CooperativeSchema)
def create_cooperative(*, db: Session = Depends(get_db), cooperative_in: CooperativeCreate):
    """
    Rota para criar uma nova cooperativa.
    """
    cooperative = Cooperative(**cooperative_in.model_dump())
    db.add(cooperative)
    db.commit()
    db.refresh(cooperative)
    return cooperative
