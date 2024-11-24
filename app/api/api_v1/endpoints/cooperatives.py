from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.cooperative import CooperativeCreate, CooperativeOut as CooperativeSchema
from app.models.cooperative import Cooperative
from app.utils.geocoding import get_lat_long_from_address

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
    lat_long = get_lat_long_from_address(cooperative_in.address)

    if lat_long is None:
        raise HTTPException(
            status_code=400,
            detail="Não foi possível obter coordenadas para o endereço fornecido."
        )

    cooperative = Cooperative(
        latitude=lat_long[0],
        longitude=lat_long[1],
        **cooperative_in.model_dump(exclude={"latitude", "longitude"}))

    db.add(cooperative)
    db.commit()
    db.refresh(cooperative)
    return cooperative
