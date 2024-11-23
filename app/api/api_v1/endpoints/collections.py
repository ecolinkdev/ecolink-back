from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.collection import Collection, CollectionStatus
from app.schemas.collection import CollectionCreate, CollectionUpdate, Collection as CollectionSchema
from app.api.deps import get_current_user
from app.models.user import User

router = APIRouter()


@router.post("/", response_model=CollectionSchema)
def create_collection(
        *,
        db: Session = Depends(get_db),
        collection_in: CollectionCreate,
        current_user: User = Depends(get_current_user)
):
    collection = Collection(
        user_id=current_user.id,
        **collection_in.model_dump()
    )
    db.add(collection)
    db.commit()
    db.refresh(collection)
    return collection


@router.get("/", response_model=List[CollectionSchema])
def list_collections(
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user),
        skip: int = 0,
        limit: int = 100
):
    collections = db.query(Collection).filter(
        Collection.user_id == current_user.id
    ).offset(skip).limit(limit).all()
    return collections


@router.patch("/{collection_id}", response_model=CollectionSchema)
def update_collection(
        *,
        db: Session = Depends(get_db),
        collection_id: int,
        collection_in: CollectionUpdate,
        current_user: User = Depends(get_current_user)
):
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
