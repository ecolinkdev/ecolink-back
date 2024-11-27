from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import create_access_token
from app.crud import crud_user
from app.schemas.token import TokenWithUserDetails

router = APIRouter()


class LoginRequest(BaseModel):
    username: str
    password: str


@router.post("/login", response_model=TokenWithUserDetails)
def login(
        form_data: LoginRequest,
        db: Session = Depends(get_db)
):
    """
   Autentica um usuário e retorna um token de acesso junto com detalhes do usuário.

   Este endpoint permite que usuários autenticados recebam um token JWT, que pode ser usado
   para acessar endpoints protegidos no sistema. A autenticação é baseada no email e senha
   fornecidos.

   Parâmetros:
   - `form_data`: Um objeto contendo as credenciais de login (email e senha).
   - `db`: Sessão do banco de dados injetada automaticamente.

   Fluxo:
   1. O sistema verifica se o email e senha são válidos utilizando a função `authenticate`
      do módulo `crud_user`.
   2. Se as credenciais forem inválidas, uma exceção HTTP 401 é levantada com uma mensagem
      de erro apropriada.
   3. Se as credenciais forem válidas, um token JWT é gerado com o ID do usuário como `subject`.
   4. Retorna o token de acesso, o tipo de token, e detalhes básicos do usuário (tipo, nome,
      email e documento).

   Retorna:
       - Um dicionário contendo:
         - `access_token`: O token de acesso JWT gerado.
         - `token_type`: Sempre "bearer".
         - `type`: O tipo do usuário (ex.: administrador, cliente, etc.).
         - `name`: O nome do usuário.
         - `email`: O email do usuário.
         - `document`: Documento de identificação do usuário (ex.: CPF ou CNPJ).

   Exceções:
       - HTTP 401: Credenciais inválidas ou usuário não encontrado.

   Exemplos de Uso:
   ```
   POST /login
   {
       "username": "email@exemplo.com",
       "password": "senha_secreta"
   }
   ```
   ```
   Resposta:
   {
       "access_token": "eyJhbGciOiJIUzI1NiIsInR...",
       "token_type": "bearer",
       "type": "user",
       "name": "João Silva",
       "email": "email@exemplo.com",
       "document": "123.456.789-00"
   }
   ```
   """
    user = crud_user.authenticate(
        db, email=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(subject=user.id)
    return {"access_token": access_token, "token_type": "bearer", "type": user.type, "name": user.name,
            "email": user.email, "document": user.document}
