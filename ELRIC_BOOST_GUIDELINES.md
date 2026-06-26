<elric-boost-guidelines>
=== foundation rules ===

# Elric Boost Guidelines

These guidelines are curated for Elric projects. Follow them closely to keep code generation, architecture, and developer experience consistent.

## Foundational Context

This project is an Elric framework application built with Python and FastAPI.

Primary stack:

- python - 3.12
- fastapi - >=0.135.1
- uvicorn - >=0.42.0
- sqlmodel - >=0.0.37
- alembic - >=1.13
- asyncpg - >=0.31.0
- redis[asyncio] - >=5.0
- langchain - >=1.2.12
- langgraph - >=1.1.0
- langsmith - >=0.7.20
- pydantic-settings - >=2.0
- structlog - >=24.0
- pytest - >=8.0
- pytest-asyncio - >=0.26
- ruff - >=0.15.6

## Core Rules

- Follow existing project conventions before introducing new patterns.
- Use descriptive names. Avoid generic names (`data`, `info`, `obj`).
- Reuse existing modules/components where possible.
- Keep handlers and routes thin; move orchestration to controllers/services/use-cases.

## File Generation (Critical)

- Do not manually scaffold framework components when Elric CLI already supports them.
- Always prefer Elric commands:
  - `elric make route <Name>`
  - `elric make controller <Name>`
  - `elric make model <Name>`
  - `elric make migration "<description>"`
  - `elric make request <Name>`
  - `elric make response <Name>`
  - `elric make seeder <Name>`
  - `elric make test <Name>`

## Python Naming Conventions

- Packages/modules/functions/methods/variables: `snake_case`
- Classes: `PascalCase`
- Constants: `UPPER_SNAKE_CASE`
- Exception classes must end in `Error`
- Avoid ambiguous names like `O`, `l`, `I`

## File Naming Conventions

- Filenames must be `snake_case.py`
- One main class/component per file (except tightly related DTO groups)
- Match file name to main class responsibility
  - `chat_controller.py` -> `ChatController`
  - `create_chat_request.py` -> `CreateChatRequest`

## FastAPI Guidelines

- Use `APIRouter` modules under `app/routes`
- Use typed request/response schemas with Pydantic
- Set `response_model` on endpoints
- Keep route functions small and explicit
- Use dependency injection (`Depends`) for DB/auth/services
- Use global exception handling for standardized error payloads

## API Schema Structure

- Keep API contracts explicit:
  - `app/schemas/requests/` for request DTOs
  - `app/schemas/responses/` for response DTOs
- Do not expose database models directly as API response contracts.

## AI Schema Structure

- Keep AI structured outputs near AI domain:
  - `app/ai/outputs/` for LLM structured output models
- Keep API DTOs and AI output DTOs separated.

## Architecture Guidelines

Use a layered modular architecture:

- `app/routes` -> HTTP layer
- `app/controllers` -> orchestration layer
- `app/ai` -> AI logic (agents/chains/tools/outputs)
- `app/providers` and `app/middleware` -> infrastructure wiring
- `database/models` and `database/migrations` -> persistence

When feasible, prefer hexagonal principles:

- Define ports/interfaces in domain/application boundaries
- Implement adapters for external systems (LLM providers, DB, cache, vector stores)
- Keep use cases independent from provider SDK details

## Database Guidelines

- Use SQLModel + async session; avoid raw SQL for normal operations
- Generate migrations via CLI/Alembic after model changes
- Keep seeders idempotent
- Run seeders through:
  - `elric db seed`

## Quality and Verification

- Run lint and formatting before finalizing changes:
  - `elric lint`
  - `elric format`
- Run focused tests for changed behavior first, then broader suites if needed.

## Logging and Errors

- Use `structlog` for structured logging
- Include event names and useful context fields
- Avoid `print()` in application code
- Raise typed exceptions and let global handlers shape HTTP responses

## Configuration

- Use `config/settings.py` (`BaseSettings`) for configuration
- Do not read environment variables directly in business code
- Keep defaults development-friendly and production-safe

## Replies and Explanations

- Be concise and practical
- Prefer step-by-step instructions when explaining workflows
- Show realistic command examples

=== elric rules ===

# Elric CLI Workflow

- Check available commands with `elric --help`, `elric make --help`, etc.
- Prefer command composition over manual edits where supported.
- For model scaffolding combos, use options such as:
  - `elric make model Chat --migration --route --controller --request --response`

=== fastapi rules ===

# FastAPI Conventions

- Version API paths with `/api/v1/...` when adding business endpoints
- Keep health endpoints lightweight and dependency-safe
- Validate all input with Pydantic models
- Return predictable response shapes

=== testing rules ===

# Testing Enforcement

- Every behavior change should be tested (new or updated tests)
- Run the minimum set of relevant tests quickly, then broaden if needed
- Do not delete tests without explicit approval

</elric-boost-guidelines>
