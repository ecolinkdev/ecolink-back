from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.crud import crud_user
from app.schemas.user import UserCreate, User

router = APIRouter()


@router.post("/", response_model=User, status_code=201)
def create_user(user_in: UserCreate, db: Session = Depends(get_db)):
    """
    Rota para criar um novo usuário.
    """

    # Verifica se o email já está em uso
    existing_user = db.query(crud_user.User).filter_by(email=user_in.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Cria o usuário no banco de dados
    user = crud_user.create(db=db, obj_in=user_in)
    return user
