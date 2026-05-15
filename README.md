# 📝 Todo API - FastAPI

API de gerenciamento de tarefas (Todo) com autenticação JWT, banco de dados relacional, migrações com Alembic e notificações por e-mail via Apache Kafka. Ambiente completo rodando via Docker Compose.

---

## 🚀 Tecnologias

* **FastAPI** — framework web principal
* **SQLAlchemy** — ORM para acesso ao banco
* **Pydantic v2 + pydantic-settings** — validação de dados e carregamento de `.env`
* **JWT (python-jose)** — autenticação com access e refresh token
* **Alembic** — migrações de banco de dados
* **PostgreSQL** — banco de dados relacional
* **Apache Kafka** — mensageria para notificações por e-mail
* **Uvicorn** — servidor ASGI
* **Docker + Docker Compose** — ambiente containerizado completo

---

## 📦 Funcionalidades

* Cadastro de usuários
* Login com JWT (access + refresh token)
* CRUD de tarefas
* Notificação por e-mail ao criar uma tarefa (via Kafka)
* Paginação (`page`, `page_size`)
* Filtros (`completed`)
* Migrações de banco com Alembic

---

## ⚙️ Pré-requisitos

* Docker
* Docker Compose v2+

> Não é necessário ter Python ou PostgreSQL instalados localmente. Tudo roda dentro dos containers.

---

## 🔧 Instalação e execução

```bash
git clone https://github.com/marciomirandas/todo-fastapi
cd todo-fastapi
cp .env.example .env
docker compose up --build
```

Para rodar em background:

```bash
docker compose up -d --build
```

---

## 🛢️ Serviços Docker

O `docker-compose.yml` sobe os seguintes serviços:

| Serviço | Descrição | Porta |
|---------|-----------|-------|
| `api` | Aplicação FastAPI | `8001` |
| `postgres` | Banco de dados PostgreSQL | `5432` |
| `zookeeper` | Coordenação do Kafka | `2181` |
| `kafka` | Broker de mensagens | `29092` |

O serviço `api` aguarda o `postgres` e o `kafka` estarem saudáveis antes de iniciar (via `healthcheck`).

---

## 🔐 Variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto:

```env
# Banco de dados
DATABASE_URL=postgresql://usuario:senha@postgres:5432/todo_db

# JWT
SECRET_KEY=sua_chave_secreta_aqui
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# PostgreSQL (usado pelo serviço postgres no Docker Compose)
POSTGRES_USER=usuario
POSTGRES_PASSWORD=senha
POSTGRES_DB=todo_db

# Kafka
KAFKA_BOOTSTRAP_SERVERS=kafka:29092
KAFKA_TOPIC_TASK_CREATED=task-created
```

> Os hosts devem usar os nomes dos serviços do Docker Compose (`postgres`, `kafka`), não `localhost`.

---

## 🔄 Migrações com Alembic

As migrações rodam automaticamente ao subir o container. Caso precise rodá-las manualmente:

```bash
# Dentro do container da API
docker compose exec api alembic upgrade head
```

### Gerar nova migration após alterar models:

```bash
docker compose exec api alembic revision --autogenerate -m "descricao"
docker compose exec api alembic upgrade head
```

---

## ▶️ Rodando localmente (sem Docker)

Se preferir rodar sem Docker:

```bash
python -m venv venv
source venv/bin/activate        # Linux/macOS
venv\Scripts\activate           # Windows

pip install -r requirements.txt
uvicorn main:app --reload
```

> Nesse caso, configure `DATABASE_URL` e `KAFKA_BOOTSTRAP_SERVERS` apontando para instâncias locais.

---

## 📖 Documentação automática

Com o projeto rodando, acesse:

```
http://localhost:8001/docs      # Swagger UI
http://localhost:8001/redoc     # ReDoc
```

---

## 🔐 Autenticação

### Login retorna:

```json
{
  "access_token": "...",
  "refresh_token": "..."
}
```

Use o token nas requisições:

```
Authorization: Bearer <access_token>
```

---

## 📚 Endpoints

### Auth

| Método | Rota | Descrição |
|--------|------|-----------|
| `POST` | `/register` | Cadastro de usuário |
| `POST` | `/login` | Login e geração de tokens |
| `POST` | `/refresh` | Renovar access token |

### Tasks

| Método | Rota | Descrição |
|--------|------|-----------|
| `POST` | `/tasks` | Criar tarefa + dispara e-mail via Kafka |
| `GET` | `/tasks` | Listar tarefas |
| `GET` | `/tasks/{id}` | Buscar tarefa por ID |
| `PUT` | `/tasks/{id}` | Atualizar tarefa |
| `DELETE` | `/tasks/{id}` | Deletar tarefa |

---

## 🔍 Paginação e filtros

```bash
# Paginação
GET /tasks?page=1&page_size=10

# Filtro por status
GET /tasks?completed=true

# Combinado
GET /tasks?page=1&page_size=5&completed=false
```

---

## 📨 Notificações com Kafka

Ao criar uma nova tarefa (`POST /tasks`), a API publica uma mensagem no tópico `task-created`. Um consumer processa essa mensagem de forma assíncrona e envia um e-mail de confirmação para o endereço do usuário autenticado.

### Fluxo

```
POST /tasks
    └─▶ Salva no PostgreSQL
    └─▶ Publica no tópico Kafka: task-created
            └─▶ Consumer consome a mensagem
                    └─▶ Envia e-mail para o usuário autenticado
```

### Tópicos

| Tópico | Evento | Descrição |
|--------|--------|-----------|
| `task-created` | Tarefa criada | Dispara e-mail de confirmação ao usuário |

> O Kafka e o Zookeeper sobem automaticamente com o Docker Compose. Nenhuma configuração adicional é necessária para o ambiente de desenvolvimento.

---

## 🧪 Testes

A API possui testes automatizados cobrindo **100% das funcionalidades**.

### ✔️ Cobertura inclui:

* Autenticação (JWT)
* CRUD de tarefas
* Publicação de eventos no Kafka
* Paginação e filtros
* Tratamento de erros (`400`, `401`, `404`)
* Segurança (acesso inválido e usuários diferentes)
* Dependências (`get_db`, `get_current_user`)

### ⚙️ Ambiente de testes

* SQLite em memória (`:memory:`)
* Kafka mockado (sem broker real)
* Isolamento total do banco principal
* Reset automático a cada teste

### 🚀 Executar testes

```bash
# Dentro do container
docker compose exec api pytest

# Localmente (com venv ativo)
pytest
```

Cobertura:

```bash
docker compose exec api coverage run -m pytest
docker compose exec api coverage report -m
```

---

## 📦 Dependências principais (`requirements.txt`)

| Pacote | Versão | Finalidade |
|--------|--------|------------|
| `fastapi` | 0.115.12 | Framework web |
| `uvicorn[standard]` | 0.34.3 | Servidor ASGI |
| `sqlalchemy` | 2.0.41 | ORM |
| `psycopg2-binary` | 2.9.10 | Driver PostgreSQL |
| `alembic` | 1.14.1 | Migrações de banco |
| `pydantic` | 2.11.4 | Validação de dados |
| `pydantic-settings` | 2.9.1 | Carregamento de `.env` |
| `python-jose[cryptography]` | 3.3.0 | JWT |
| `passlib[bcrypt]` | 1.7.4 | Hash de senhas |
| `python-dotenv` | 1.1.0 | Variáveis de ambiente |
| `kafka-python` | 2.0.2 | Producer/Consumer Kafka |
| `httpx` | 0.28.1 | Cliente HTTP (testes) |
| `pytest` | 8.3.5 | Testes |
| `pytest-asyncio` | 0.26.0 | Testes assíncronos |
| `coverage` | 7.8.0 | Cobertura de testes |