# **Ecolink Backend**

_Ecolink é uma plataforma para melhorar os ganhos financeiros e a qualidade de vida dos catadores de materiais
recicláveis._

## **Índice**

1. [Visão Geral](#visão-geral)
2. [Tecnologias Utilizadas](#tecnologias-utilizadas)
3. [Requisitos](#requisitos)
4. [Configuração do Projeto](#configuração-do-projeto)
5. [Como Rodar o Projeto](#como-rodar-o-projeto)
6. [Estrutura de Diretórios](#estrutura-de-diretórios)
7. [Endpoints Principais](#endpoints-principais)
8. [Contribuindo](#contribuindo)
9. [Licença](#licença)

---

## **Visão Geral**

O backend do Ecolink foi desenvolvido com **FastAPI**, proporcionando uma API robusta e escalável para atender as
funcionalidades do sistema.  
A plataforma conecta catadores de recicláveis a cooperativas, facilitando o gerenciamento de coletas e o impacto
ambiental.

---

## **Tecnologias Utilizadas**

- **Python 3.10+**: Linguagem de programação principal.
- **FastAPI**: Framework web para criação da API.
- **PostgreSQL**: Banco de dados relacional.
- **SQLAlchemy**: ORM para interação com o banco de dados.
- **Docker**: Para containerização do ambiente.
- **Alembic**: Gerenciamento de migrações do banco de dados.
- **Pydantic**: Validação e parsing de dados.
- **Nominatim API**: Para geocodificação (obtenção de coordenadas geográficas a partir de endereços).

---

## **Requisitos**

Certifique-se de ter as seguintes ferramentas instaladas:

- **Python 3.10+**
- **Docker** e **Docker Compose** (opcional, para ambiente de desenvolvimento containerizado)
- **PostgreSQL** (se não estiver utilizando Docker)

---

## **Configuração do Projeto**

### 1. Clonar o Repositório

```bash
git clone https://github.com/seu-usuario/ecolink-backend.git
cd ecolink-backend
```

### 2. Configurar Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto e adicione as seguintes configurações:

```plaintext
# Nome do projeto
PROJECT_NAME=Ecolink Backend

# Chave secreta para autenticação
SECRET_KEY=sua-chave-secreta

# Algoritmo usado para tokens JWT
ALGORITHM=HS256

# Expiração do token (em minutos)
ACCESS_TOKEN_EXPIRE_MINUTES=1440

# Configuração do banco de dados PostgreSQL
POSTGRES_SERVER=localhost
POSTGRES_USER=seu-usuario
POSTGRES_PASSWORD=sua-senha
POSTGRES_DB=ecolink

# Configuração de CORS (origens permitidas)
BACKEND_CORS_ORIGINS=http://localhost:3000,http://seu-site.com
```

Nota:
Substitua sua-chave-secreta, seu-usuario, sua-senha e http://seu-site.com pelos valores específicos do seu ambiente.

Se preferir permitir todas as origens de CORS durante o desenvolvimento, configure:

```plaintext
BACKEND_CORS_ORIGINS=*
```

Atenção:
Não utilize `*` em produção, pois isso permite qualquer origem acessar a API, o que pode ser inseguro.

### 3. Instalar Dependências

```bash
pip install -r requirements.txt
```

## Como Rodar o Projeto

Siga as etapas abaixo para rodar o projeto localmente:

### 1. Clone o Repositório

Clone o repositório para a sua máquina local:

```bash
git clone https://github.com/seu-usuario/seu-repositorio.git
cd seu-repositorio
```

### 2. Crie e Ative o Ambiente Virtual

Crie um ambiente virtual Python e ative-o:

```bash
# Crie o ambiente virtual
python -m venv venv

# Ative o ambiente virtual no Linux/MacOS
source venv/bin/activate

# Ative o ambiente virtual no Windows
venv\Scripts\activate
```

### 3. Instale as Dependências

Instale as dependências do projeto listadas no arquivo `requirements.txt`:

```bash
pip install -r requirements.txt
```

### 4. Configure o Banco de Dados

Certifique-se de que o banco de dados PostgreSQL está configurado corretamente e que as variáveis de ambiente no arquivo
`.env` estão corretas. Para criar o esquema inicial no banco de dados, execute::

```bash
alembic revision --autogenerate -m "Initial Migrations"
```

Revise o migrate inicial e depois execute:

```bash
alembic upgrade head
```

### 5. Execute o Servidor de Desenvolvimento

Inicie o servidor FastAPI:

```bash
uvicorn app.main:app --reload
```

O servidor estará disponível no endereço http://127.0.0.1:8000.

### 6. Acesse a Documentação da API

Acesse a documentação interativa da API utilizando o Swagger UI ou o Redoc:

- Swagger UI: http://127.0.0.1:8000/docs
- Redoc: http://127.0.0.1:8000/redoc

### Estrutura de Diretórios

Abaixo está a estrutura de diretórios do projeto para facilitar a navegação:

```plaintext
.
├── alembic/               # Diretório de configuração e migrações do Alembic
│   ├── versions/          # Arquivos de migração do banco de dados
│   ├── env.py             # Arquivo principal do Alembic
│   └── script.py.mako     # Template para novas migrações
├── app/                   # Diretório principal da aplicação
│   ├── api/               # Rotas e endpoints da API
│   │   ├── api_v1/        # Versão 1 da API
│   │   │   ├── endpoints/ # Endpoints individuais (users, collections, etc.)
│   │   │   │   ├── __init__.py
│   │   │   │   └── api.py # Roteador principal da API v1
│   │   │   ├── __init__.py
│   │   │   └── deps.py    # Configurações JWT 
│   ├── core/              # Configurações centrais do sistema
│   │   ├── config.py      # Configuração do projeto e variáveis globais
│   │   ├── database.py    # Configuração do banco de dados
│   │   └── security.py    # Funções de segurança (autenticação, tokens, etc.)
│   ├── crud/              # Operações de banco de dados (CRUD)
│   │   ├── crud_user.py   # Operações específicas para o modelo User
│   │   └── __init__.py
│   ├── models/            # Modelos SQLAlchemy que representam tabelas no banco de dados
│   │   ├── user.py        # Modelo User
│   │   ├── collection.py  # Modelo Collection
        ├── cooperative.py # Modelo Cooperative
│   │   └── __init__.py
│   ├── schemas/           # Schemas Pydantic para validação de entrada/saída
│   │   ├── user.py        # Schemas para User
│   │   ├── collection.py  # Schemas para Collection
│   │   ├── cooperative.py # Schemas para Cooperative
│   │   ├── token.py       # Schemas para Token
│   │   └── __init__.py
│   ├── utils/             # Funções auxiliares e utilitárias
│   │   ├── geocoding.py   # Funções para trabalhar com geocodificação
│   │   └── __init__.py
│   ├── main.py            # Arquivo principal da aplicação (ponto de entrada)
│   └── __init__.py
├── .env                   # Arquivo de variáveis de ambiente
├── requirements.txt       # Lista de dependências do projeto
├── alembic.ini            # Configuração do Alembic
└── README.md              # Documentação do projeto
```

### Endpoints Principais

#### Autenticação

- **POST /api/v1/login/**
    - **Descrição**: Faz login e retorna um token de autenticação.
    - **Parâmetros**:
        - `username` (string): O email do usuário.
        - `password` (string): A senha do usuário.
    - **Resposta**:
        - `access_token`: Token de autenticação.
        - `token_type`: Tipo do token (bearer).
        - `type`: Tipo de usuário.
        - `name`: Nome do usuário.
        - `email`: Email do usuário.
        - `document`: Documento do usuário.

#### Usuários

- **POST /api/v1/users/**
    - **Descrição**: Cria um novo usuário.
    - **Parâmetros**:
        - `name` (string): Nome do usuário.
        - `email` (string): Email do usuário.
        - `password` (string): Senha do usuário.
        - `type` (string): Tipo de usuário (ex: "residential" ou "commercial").
    - **Resposta**:
        - `id`: ID do usuário criado.
        - `name`: Nome do usuário.
        - `email`: Email do usuário.

- **GET /api/v1/users/me/**
    - **Descrição**: Retorna informações do usuário autenticado.
    - **Resposta**:
        - `id`: ID do usuário autenticado.
        - `name`: Nome do usuário.
        - `email`: Email do usuário.
        - Outros campos definidos no modelo de usuário.

#### Coletas

- **POST /api/v1/collections/**
    - **Descrição**: Cria uma nova coleta.
    - **Parâmetros**:
        - `address` (string): Endereço da coleta.
        - `materials` (array): Lista de materiais a serem coletados.
        - `status` (string): Status da coleta (ex: "pending").
    - **Resposta**:
        - `id`: ID da coleta criada.
        - `user_id`: ID do usuário associado à coleta.
        - `address`: Endereço da coleta.
        - `latitude`: Latitude do endereço.
        - `longitude`: Longitude do endereço.
        - `materials`: Materiais a serem coletados.
        - `status`: Status da coleta.

- **GET /api/v1/collections/**
    - **Descrição**: Lista as coletas do usuário autenticado.
    - **Resposta**:
        - Lista de coletas associadas ao usuário autenticado.

- **GET /api/v1/collections/all/**
    - **Descrição**: Lista todas as coletas.
    - **Resposta**:
        - Lista de todas as coletas cadastradas no sistema.

#### Cooperativas

- **POST /api/v1/cooperatives/**
    - **Descrição**: Cria uma nova cooperativa.
    - **Parâmetros**:
        - `name` (string): Nome da cooperativa.
        - `address` (string): Endereço da cooperativa.
    - **Resposta**:
        - `id`: ID da cooperativa criada.
        - `name`: Nome da cooperativa.
        - `address`: Endereço da cooperativa.

- **GET /api/v1/cooperatives/**
    - **Descrição**: Lista todas as cooperativas.
    - **Resposta**:
        - Lista de todas as cooperativas cadastradas no sistema.

## Contribuindo

Contribuições são bem-vindas! Para contribuir, siga os seguintes passos:

1. Faça um fork do repositório.
2. Crie uma branch para sua feature ou correção:

```bash
git checkout -b minha-feature
```

3. Adicione todas as mudanças:

```bash 
git add .
```

3. Faça o commit das mudanças:

```bash 
git commit -m 'Adiciona minha nova feature'
```

4. Envie o push para a branch:

```bash 
git push origin minha-feature
```

5. Abra um Pull Request no repositório original.

## Licença

Este projeto está licenciado sob a licença [MIT](https://opensource.org/licenses/MIT). Veja o arquivo [LICENSE](LICENSE) para mais detalhes.
