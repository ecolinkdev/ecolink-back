from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.crud import crud_user
from app.schemas.user import UserCreate, User

router = APIRouter()


@router.post("/", response_model=User, status_code=201)
def create_user(user_in: UserCreate, db: Session = Depends(get_db)):
    """
    Cria um novo usuário no sistema.

    Este endpoint é usado para registrar novos usuários no banco de dados. Ele valida se o
    email fornecido já está registrado e, caso contrário, cria um novo registro com as
    informações fornecidas.

    Parâmetros:
    - `user_in`: Um objeto contendo os dados do novo usuário a ser criado (nome, email, senha, etc.).
    - `db`: Sessão do banco de dados injetada automaticamente.

    Fluxo:
    1. Verifica se já existe um usuário com o email fornecido.
    2. Caso o email já esteja registrado, uma exceção HTTP 400 é levantada com uma mensagem apropriada.
    3. Se o email não estiver em uso, o usuário é criado no banco de dados utilizando o CRUD de usuários.
    4. Retorna o objeto do usuário criado, excluindo informações sensíveis (como a senha).

    Retorna:
        - Um objeto representando o usuário criado:
          - `id`: Identificador único do usuário.
          - `name`: Nome do usuário.
          - `email`: Email registrado do usuário.
          - Outros campos definidos no modelo de retorno.

    Exceções:
        - HTTP 400: Levantada caso o email fornecido já esteja registrado.

    Exemplos de Uso:
    ```
    POST /users/
    {
        "email": "joao.silva@exemplo.com",
        "name": "João Silva",
        "type": "residential" or "commercial",
        "address": "Rua 2",
        "phone": "999999999",
        "document": "404",
        "password": "senha_segura123",
    }
    ```
    ```
    Resposta:
    {
        "email": "joao.silva@exemplo.com",
        "name": "João Silva",
        "type": "residential",
        "address": "Rua 2",
        "phone": "999999999",
        "document": "404",
        "id": 4,
        "created_at": "2024-11-27T14:05:30.319717Z"
    }
    ```
    """

    # Verifica se o email já está em uso
    existing_user = db.query(crud_user.User).filter_by(email=user_in.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Cria o usuário no banco de dados
    user = crud_user.create(db=db, obj_in=user_in)
    return user
