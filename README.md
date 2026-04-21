# API de Gerenciamento de Equipamentos

API REST desenvolvida com FastAPI para gerenciamento de equipamentos, com autenticação via JWT e controle de acesso por usuário.

## Visão Geral

Esta API permite o cadastro de usuários, autenticação e gerenciamento de equipamentos de forma segura. Cada usuário possui acesso apenas aos seus próprios dados.

## Tecnologias Utilizadas

* Python 3.12
* FastAPI
* SQLAlchemy
* SQLite
* JWT (JSON Web Token)
* Passlib (hash de senha)
* Uvicorn

## Funcionalidades

* Cadastro de usuários
* Autenticação com geração de token JWT
* CRUD completo de equipamentos
* Proteção de rotas com autenticação
* Isolamento de dados por usuário (multi-tenant básico)
* Validação de permissões (somente o usuário logado pode acessar/modificar/deletar)

## Estrutura do Projeto

```
app/
├── database/
│   └── connection.py
├── models/
│   ├── user.py
│   └── equipamento.py
├── routes/
│   ├── auth.py
│   └── equipamentos.py
├── schemas/
│   ├── user.py
│   └── equipamento.py
├── services/
│   ├── auth.py
│   └── security.py
└── main.py
```

## Como Executar o Projeto

### 1. Clonar o repositório

```bash
git clone https://github.com/arthurrguedes/equipamentos-api.git
cd equipamentos-api
```

### 2. Criar ambiente virtual

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

### 3. Instalar dependências

```bash
pip install -r requirements.txt
```

### 4. Executar a aplicação

```bash
uvicorn app.main:app --reload
```

A API estará disponível em:
http://127.0.0.1:8000

Documentação interativa:
http://127.0.0.1:8000/docs

## Autenticação

A autenticação é feita via JWT.

### Fluxo:

1. Registrar usuário:

```
POST /auth/register
```

2. Realizar login:

```
POST /auth/login
```

3. Copiar o token retornado

4. Autorizar no Swagger:

* Clicar em "Authorize"
* Informar:

```
Bearer SEU_TOKEN_AQUI
```

## Endpoints

### Autenticação

* POST /auth/register
* POST /auth/login

### Equipamentos (protegidos)

* POST /equipamentos
* GET /equipamentos
* GET /equipamentos/{id}
* PUT /equipamentos/{id}
* DELETE /equipamentos/{id}

## Regras de Negócio

* Cada equipamento pertence a um usuário
* Usuários só podem acessar seus próprios equipamentos
* A API retorna erro 404 para recursos inexistentes
* Rotas protegidas exigem token válido

## Exemplo de Requisição

### Criar equipamento

```
POST /equipamentos
Authorization: Bearer TOKEN
```

```json
{
  "nome": "Notebook",
  "status": "ativo"
}
```

## Possíveis Melhorias

* Paginação de resultados
* Filtros por status e nome
* Relacionamento ORM com retorno de dados do usuário
* Deploy em ambiente de produção
* Containerização com Docker

## Autor

Arthur Guedes Sant'anna
