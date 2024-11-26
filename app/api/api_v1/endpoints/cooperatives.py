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
    Recupera a lista de todas as cooperativas cadastradas no sistema.

    Este endpoint permite a visualização de todas as cooperativas disponíveis no banco de dados.
    Ele é útil para exibir informações sobre cooperativas para os usuários do sistema ou administradores.

    Paginação é suportada pelos seguintes parâmetros:
    - `skip`: Número de registros a serem ignorados no início da lista (default: 0).
    - `limit`: Número máximo de registros a serem retornados (default: 100).

    Retorna:
        - Uma lista de todas as cooperativas registradas no sistema, paginada conforme os parâmetros fornecidos.
    """
    cooperatives = db.query(Cooperative).offset(skip).limit(limit).all()
    return cooperatives


@router.post("/", response_model=CooperativeSchema)
def create_cooperative(*, db: Session = Depends(get_db), cooperative_in: CooperativeCreate):
    """
    Cria uma nova cooperativa e salva no banco de dados.

    Este endpoint permite cadastrar uma nova cooperativa no sistema.
    O endereço fornecido é usado para obter as coordenadas geográficas (latitude e longitude) por meio de uma API externa.
    Se a geocodificação do endereço falhar, uma exceção será levantada.

    Parâmetros:
    - `cooperative_in`: Dados da cooperativa a ser criada, fornecidos pelo cliente no formato `CooperativeCreate`.

    Regras:
    - O endereço deve ser válido para permitir a obtenção de coordenadas.
    - O sistema armazena automaticamente a latitude e longitude no registro da cooperativa.

    Retorna:
        - Os detalhes da cooperativa recém-criada, incluindo as coordenadas calculadas.

    Exceções:
        - Retorna um erro HTTP 400 se não for possível geocodificar o endereço.
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
