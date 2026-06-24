# Elric Framework

Opinionated Python framework for AI-first applications with FastAPI, LangGraph, and LangChain.

## Stack Tecnologico

- **FastAPI** - Web framework
- **LangGraph** - Agentic workflows
- **LangChain** - AI chains e tools
- **LangSmith** - Tracing e monitoring
- **SQLModel** - ORM (Pydantic + SQLAlchemy)
- **Alembic** - Database migrations
- **PostgreSQL** - Database relazionale
- **Redis** - Cache e rate limiting
- **Structlog** - Logging strutturato JSON
- **uv** - Package manager

## Prerequisiti

- Python 3.12+
- PostgreSQL 16+
- Redis 7+
- [uv](https://github.com/astral-sh/uv) package manager

## Setup Iniziale

### 1. Clona il repository

```bash
git clone <repository-url>
cd elric_framework
```

### 2. Installa le dipendenze

```bash
uv sync
```

### 3. Configura le variabili d'ambiente

Copia il file `.env.example` in `.env` e modifica i valori:

```bash
cp .env.example .env
```

Modifica `.env` con le tue configurazioni:

```env
# Database
DATABASE_URL=postgresql+asyncpg://elric:secret@localhost:5432/elric_dev

# Redis
REDIS_URL=redis://localhost:6379/0

# LangSmith (opzionale)
LANGCHAIN_TRACING_V2=false
LANGCHAIN_API_KEY=
LANGCHAIN_PROJECT=elric-app
```

### 4. Avvia i servizi Docker (Database e Redis)

```bash
docker compose -f docker/docker-compose.yml up -d db redis
```

Questo avvierà PostgreSQL e Redis in background.

### 5. Esegui le migrations del database

```bash
uv run alembic upgrade head
```

### 6. (Opzionale) Installa il comando `elric` globalmente

Per usare `elric` come comando globale invece di `uv run elric`:

```bash
elric_cli/install.sh
```

Questo creerà un wrapper che ti permette di usare `elric` da qualsiasi directory:

```bash
elric --help
elric make agent MyAgent
elric serve
```

**Nota**: Se `~/.local/bin` non è nel tuo PATH, aggiungi questa riga al tuo `~/.zshrc` o `~/.bashrc`:

```bash
export PATH="$HOME/.local/bin:$PATH"
```

Poi ricarica la shell:

```bash
source ~/.zshrc  # o source ~/.bashrc
```

Per disinstallare il comando globale:

```bash
elric_cli/uninstall.sh
```

## Avvio dell'Applicazione

### Sviluppo locale (Raccomandato)

```bash
# Avvia database e redis in Docker
docker compose -f docker/docker-compose.yml up -d db redis

# Esegui l'app localmente con hot-reload
uv run uvicorn app:create_app --factory --reload --host 0.0.0.0 --port 8000
```

L'applicazione sarà disponibile su:

- API: http://localhost:8000
- Docs (Swagger): http://localhost:8000/docs
- Health check: http://localhost:8000/health

**Nota**: Le richieste da `localhost` non richiedono API key per facilitare lo sviluppo.

### Con Docker Compose (tutto containerizzato)

Se preferisci eseguire anche l'app in Docker:

```bash
# Avvia tutti i servizi
docker compose -f docker/docker-compose.yml up -d

# Visualizza i logs
docker compose -f docker/docker-compose.yml logs -f elric

# Ferma i servizi
docker compose -f docker/docker-compose.yml down
```

**Nota**: Se esegui l'app in Docker, modifica `.env` per usare i nomi dei servizi invece di `localhost`:

```env
DATABASE_URL=postgresql+asyncpg://elric:secret@db:5432/elric_dev
REDIS_URL=redis://redis:6379/0
```

### Produzione

```bash
uv run gunicorn app:create_app --factory -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

## Gestione API Keys

### Creare una nuova API Key

**Con la CLI** (metodo raccomandato):

```bash
# Se hai installato elric globalmente
elric apikey create "My App Name"

# Oppure con uv run
uv run elric apikey create "My App Name"
```

**Con uno script Python**:

```python
# create_api_key.py
import asyncio
from app.providers.database import AsyncSessionLocal
from app.utils.api_key import create_api_key_record

async def main():
    async with AsyncSessionLocal() as session:
        api_key_record, key = await create_api_key_record("My App Name", session)
        print(f"✅ API Key created successfully!")
        print(f"ID: {api_key_record.id}")
        print(f"Name: {api_key_record.name}")
        print(f"Key: {key}")
        print(f"\n🔑 Save this key securely - it won't be shown again!")
        print(f"\nExample usage:")
        print(f'curl -H "X-API-Key: {key}" http://localhost:8000/docs')

if __name__ == "__main__":
    asyncio.run(main())
```

Esegui lo script:

```bash
uv run python create_api_key.py
```

**⚠️ IMPORTANTE**: Salva la chiave generata in un posto sicuro. Non verrà mostrata di nuovo.

### Listare tutte le API Keys

```bash
elric apikey list
```

### Revocare una API Key

```bash
elric apikey revoke <key-id>
```

### Usare l'API Key

L'API key è richiesta solo per richieste esterne. Le richieste da `localhost` non richiedono autenticazione per facilitare lo sviluppo.

Per testare con API key:

```bash
curl -H "X-API-Key: elk_live_xxxxx" http://your-domain.com/api/endpoint
```

**Nota**: Durante lo sviluppo locale, puoi accedere a tutti gli endpoint senza API key:

```bash
curl http://localhost:8000/docs
```

## Database Migrations

### Creare una nuova migration

**Con la CLI**:

```bash
elric make migration "descrizione_migration"
```

**Con Alembic direttamente**:

```bash
uv run alembic revision --autogenerate -m "descrizione_migration"
```

### Applicare le migrations

```bash
elric migrate
# oppure: uv run alembic upgrade head
```

### Rollback ultima migration

```bash
elric migrate rollback
# oppure: uv run alembic downgrade -1
```

### Verificare stato migrations

```bash
elric migrate status
# oppure: uv run alembic current
```

### Drop tutto e re-migra (⚠️ ATTENZIONE: cancella tutti i dati)

```bash
elric migrate fresh
```

## CLI Commands

Elric fornisce una CLI completa per generare componenti e gestire l'applicazione.

### Generazione Componenti (make:\*)

#### Agent con Tipi e Modelli

Elric supporta diversi tipi di agent con configurazione del modello LLM:

```bash
# Genera un simple agent (default) con GPT-4o (default)
elric make agent MyAgent

# Genera un chat agent con memoria conversazionale
elric make agent CustomerSupport --type=chat --model=claude-3-5-sonnet

# Genera un tool agent che può usare tools
elric make agent ResearchAssistant --type=tool --model=gpt-4o

# Genera un ReAct agent (Reasoning + Acting)
elric make agent DataAnalyzer --type=react --model=gpt-4-turbo

# Genera un planner agent per task complessi
elric make agent TaskPlanner --type=planner --model=gemini-1.5-pro

# Genera un streaming agent per risposte in tempo reale
elric make agent StreamBot --type=streaming --model=claude-3-opus
```

**Tipi di Agent Disponibili:**

- `simple` - Agent base semplice (default)
- `chat` - Agent conversazionale con memoria
- `tool` - Agent che può usare tools
- `react` - Agent con reasoning e acting
- `planner` - Agent per pianificazione task complessi
- `streaming` - Agent con supporto streaming

**Modelli Supportati:**

- **Anthropic**: `claude-3-5-sonnet`, `claude-3-opus`, `claude-3-haiku`
- **OpenAI**: `gpt-4o`, `gpt-4-turbo`, `gpt-4`, `gpt-3.5-turbo`
- **Google**: `gemini-1.5-pro`, `gemini-1.5-flash`, `gemini-pro`
- **Cohere**: `command-r-plus`, `command-r`, `command`

#### Altri Componenti

```bash
# Genera una nuova LangChain chain
elric make chain SummaryChain

# Genera un nuovo LangChain tool
elric make tool WebSearchTool

# Genera un nuovo FastAPI router
elric make route UserRoute

# Genera un nuovo controller
elric make controller UserController

# Genera un nuovo Pydantic schema
elric make schema UserSchema

# Genera un nuovo SQLModel entity
elric make model User

# Genera un nuovo background job
elric make job EmailJob

# Genera una nuova custom exception
elric make exception CustomException

# Genera un nuovo test file
elric make test UserTest
```

### Comandi Server

```bash
# Avvia il server di sviluppo con hot-reload
elric serve

# Avvia su porta personalizzata
elric serve --port 3000

# Avvia senza hot-reload
elric serve --no-reload
```

### Comandi Route

```bash
# Lista tutte le routes registrate
elric route list
```

### Tutti i comandi disponibili

```bash
# Mostra tutti i comandi
elric --help

# Mostra aiuto per un gruppo di comandi
elric make --help
elric migrate --help
elric apikey --help
```

## Struttura del Progetto

```
elric_framework/
├── app/
│   ├── ai/              # AI Components
│   │   ├── agents/      # LangGraph agents
│   │   ├── chains/      # LangChain chains
│   │   ├── tools/       # LangChain tools
│   │   ├── memory/      # Memory management
│   │   ├── vectorstore/ # Vector databases
│   │   └── middleware/  # AI-specific middleware
│   ├── routes/          # FastAPI routes
│   ├── controllers/     # Business logic
│   ├── middleware/      # HTTP middleware
│   ├── providers/       # Database, Redis, LangSmith
│   ├── schemas/         # Pydantic schemas
│   ├── exceptions/      # Custom exceptions
│   ├── jobs/            # Background jobs
│   ├── events/          # Event handlers
│   └── utils/           # Utility functions
├── config/              # Configuration
├── database/
│   ├── models/          # SQLModel entities
│   ├── migrations/      # Alembic migrations
│   └── seeders/         # Database seeders
├── tests/
│   ├── unit/
│   ├── integration/
│   └── e2e/
├── elric_cli/           # CLI tools
│   ├── commands/        # CLI commands
│   ├── install.sh       # Global installation
│   └── uninstall.sh     # Uninstallation
├── docker/              # Docker configs
└── stubs/               # Code generation templates
```

## Features Implementate

### ✅ Fase 1 - Scaffolding

- Struttura progetto completa
- Docker Compose per sviluppo
- Configurazione uv e pyproject.toml

### ✅ Fase 2 - App Base

- FastAPI app con lifespan
- Providers: Database (PostgreSQL), Redis, LangSmith
- Health check endpoint
- Configurazione centralizzata con Pydantic Settings

### ✅ Fase 3 - Auth + Middleware

- Autenticazione API Key con cache Redis
- Rate limiting (sliding window)
- Logging strutturato con trace_id
- Alembic configurato per migrations async

### ✅ Fase 4 - Error Handling

- Gerarchia completa di custom exceptions
- Global exception handler con risposte JSON uniformi
- Trace ID in tutte le risposte di errore
- Logging strutturato degli errori

### ✅ Fase 5 - CLI Elric

- 14 stub files per generazione componenti
- CLI completa con Typer (19 comandi)
- Comandi make:\* per generare agent, chain, tool, route, etc.
- Comandi migrate:\* che wrappano Alembic
- Comandi apikey:\* per gestione API keys
- Script di installazione globale (install.sh/uninstall.sh)

## Logging

I log sono strutturati in formato JSON (configurabile via `LOG_JSON=true/false`):

```json
{
  "timestamp": "2026-03-20T10:14:39Z",
  "level": "info",
  "event": "request.completed",
  "trace_id": "uuid-v4",
  "method": "GET",
  "path": "/health",
  "status_code": 200,
  "duration_ms": 42
}
```

Ogni richiesta ha un `trace_id` univoco propagato attraverso tutto lo stack.

## Rate Limiting

Il rate limiting usa Redis con sliding window counter:

- Default: 100 richieste per 60 secondi
- Configurabile via `RATE_LIMIT_REQUESTS` e `RATE_LIMIT_WINDOW`
- Risposta 429 quando il limite viene superato

## Testing

```bash
# Run all tests
uv run pytest tests/ -v

# Run with coverage
uv run pytest tests/ --cov=app --cov-report=html

# Run specific test file
uv run pytest tests/unit/test_api_key.py -v
```

## Linting e Formatting

```bash
# Check code style
uv run ruff check .

# Fix auto-fixable issues
uv run ruff check --fix .

# Format code
uv run ruff format .
```

## Troubleshooting

### Porta già in uso

```bash
# Trova il processo sulla porta 8000
lsof -i :8000

# Termina il processo
kill -9 <PID>
```

### Database connection error

Verifica che PostgreSQL sia in esecuzione:

```bash
docker compose -f docker/docker-compose.yml ps
```

### Redis connection error

Verifica che Redis sia in esecuzione:

```bash
docker compose -f docker/docker-compose.yml ps
redis-cli ping  # Dovrebbe rispondere PONG
```

## Prossime Fasi

- **Fase 6**: Base classes per Agents, Chains, Tools
- **Fase 7**: Windsurf rules per AI-assisted development
- **Fase 8**: Testing completo e CI/CD

## License

MIT
