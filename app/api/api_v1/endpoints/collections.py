from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.collection import Collection, CollectionStatus
from app.schemas.collection import CollectionCreate, CollectionUpdate, Collection as CollectionSchema
from app.api.deps import get_current_user
from app.models.user import User
from app.utils.geocoding import get_lat_long_from_address

router = APIRouter()


@router.post("/", response_model=CollectionSchema)
def create_collection(
        *,
        db: Session = Depends(get_db),
        collection_in: CollectionCreate,
        current_user: User = Depends(get_current_user)
):
    """
    Cria uma nova coleção associada ao usuário autenticado.

    Este endpoint permite que um usuário crie uma coleção, fornecendo os detalhes necessários
    como endereço, materiais, e status. O endereço é utilizado para obter as coordenadas de
    latitude e longitude através de uma API de geocodificação.

    Parâmetros:
    - `collection_in`: Dados da coleção a ser criada, incluindo endereço, materiais, etc.
    - `db`: Sessão do banco de dados, injetada automaticamente.
    - `current_user`: O usuário autenticado, obtido a partir do token JWT.

    Fluxo:
    1. O endereço fornecido na entrada é usado para obter as coordenadas geográficas (latitude e longitude).
    2. Se as coordenadas não puderem ser recuperadas, uma exceção HTTP 400 é lançada.
    3. Se as coordenadas forem obtidas com sucesso, a coleção é criada no banco de dados.
    4. A coleção é associada ao usuário autenticado, e as coordenadas são salvas junto com os outros dados.
    5. O novo registro da coleção é retornado.

    Retorna:
        - O objeto da coleção recém-criada, com todos os campos preenchidos, incluindo `id`, `user_id`, `latitude`, `longitude`, etc.

    Exceções:
        - HTTP 400: Caso não seja possível obter as coordenadas para o endereço fornecido.

    Exemplos de Uso:
    ```
    POST /collections/
    {
        "address": "Rua das Flores, 123",
        "date": "2024-11-26T10:00:00",
        "time": "10:00",
        "materials": [{"material": "papel", "quantity": 100, "unity": KG}],
        "status": "pending"
    }
    ```
    Resposta:
    {
        "id": 1,
        "user_id": 1,
        "address": "Rua das Flores, 123",
        "latitude": -23.5505,
        "longitude": -46.6333,
        "status": "pending",
        "created_at": "2024-11-26T10:00:00",
        "updated_at": "2024-11-26T10:00:00"
    }
    """
    lat_long = get_lat_long_from_address(collection_in.address)
    if lat_long is None:
        raise HTTPException(
            status_code=400,
            detail="Não foi possível obter coordenadas para o endereço fornecido."
        )

    collection = Collection(
        user_id=current_user.id,
        latitude=lat_long[0],
        longitude=lat_long[1],
        **collection_in.model_dump(exclude={"latitude", "longitude"})
    )
    db.add(collection)
    db.commit()
    db.refresh(collection)
    return collection


@router.get("/user", response_model=List[CollectionSchema])
def list_user_collections(
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user),
        skip: int = 0,
        limit: int = 100
):
    """
    Recupera a lista de coleções associadas ao usuário autenticado.

    Este endpoint retorna apenas as coleções criadas pelo usuário que fez o login no sistema.
    É possível paginar os resultados utilizando os parâmetros `skip` e `limit`.

    - `skip`: Número de coleções a ignorar no início (default: 0).
    - `limit`: Número máximo de coleções a retornar (default: 100).

    Retorna:
        - Uma lista de coleções pertencentes ao usuário atual.
    """
    collections = db.query(Collection).filter(
        Collection.user_id == current_user.id
    ).offset(skip).limit(limit).all()
    return collections


@router.get("/all", response_model=List[CollectionSchema])
def list_all_collections(
        db: Session = Depends(get_db),
        skip: int = 0,
        limit: int = 100
):
    """
    Recupera a lista de todas as coleções cadastradas no sistema.

    Este endpoint retorna todas as coleções disponíveis no banco de dados, independentemente do usuário que as criou.
    É útil para casos em que administradores ou usuários avançados precisam visualizar coleções de todos os usuários.
    Paginação é suportada através dos parâmetros `skip` e `limit`.

    - `skip`: Número de coleções a ignorar no início (default: 0).
    - `limit`: Número máximo de coleções a retornar (default: 100).

    Retorna:
        - Uma lista de todas as coleções registradas no sistema.
    """
    collections = db.query(Collection).offset(skip).limit(limit).all()
    return collections


@router.patch("/{collection_id}", response_model=CollectionSchema)
def update_collection(
        *,
        db: Session = Depends(get_db),
        collection_id: int,
        collection_in: CollectionUpdate,
        current_user: User = Depends(get_current_user)
):
    """
    Atualiza uma coleção existente associada ao usuário autenticado.

    Este endpoint permite que um usuário atualizado detalhes de uma coleção específica. O usuário
    pode atualizar apenas as coleções que pertencem a ele. Se a coleção não for encontrada ou se
    o usuário tentar acessar uma coleção que não lhe pertence, uma exceção HTTP 404 será gerada.

    Parâmetros:
    - `collection_id`: ID da coleção a ser atualizada.
    - `collection_in`: Dados para atualizar a coleção, incluindo os campos que desejam ser alterados.
    - `db`: Sessão do banco de dados, injetada automaticamente.
    - `current_user`: O usuário autenticado, obtido a partir do token JWT.

    Fluxo:
    1. A coleção com o ID fornecido é buscada no banco de dados e verificada se pertence ao usuário autenticado.
    2. Se a coleção não for encontrada ou não pertencer ao usuário, uma exceção HTTP 404 é lançada.
    3. Os campos fornecidos no `collection_in` são aplicados à coleção existente.
    4. O banco de dados é atualizado e a coleção modificada é retornada.

    Retorna:
        - O objeto da coleção atualizado, com todos os campos refletindo as alterações.

    Exceções:
        - HTTP 404: Se a coleção não for encontrada ou não pertencer ao usuário.

    Exemplos de Uso:
    ```
    PATCH /collections/1
    {
        "status": "completed"
    }
    ```
    Resposta:
    {
        "id": 1,
        "user_id": 1,
        "address": "Rua das Flores, 123",
        "latitude": -23.5505,
        "longitude": -46.6333,
        "status": "completed",
        "created_at": "2024-11-26T10:00:00",
        "updated_at": "2024-11-26T11:00:00"
    }
    """
    collection = db.query(Collection).filter(
        Collection.id == collection_id,
        Collection.user_id == current_user.id
    ).first()

    if not collection:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Collection not found"
        )

    for field, value in collection_in.model_dump(exclude_unset=True).items():
        setattr(collection, field, value)

    db.commit()
    db.refresh(collection)
    return collection
