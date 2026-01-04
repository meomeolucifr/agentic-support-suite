# Shared Tools

## Purpose

This directory contains shared utilities, clients, and tools that are used across all agents and services. These tools provide common functionality like database access, LLM integration, caching, and external service integrations.

## Structure

```
tools/
├── database/          # Database utilities and models
├── vector_db/         # Chroma vector database client
├── llm/               # LLM provider abstraction
├── cache/             # Redis caching utilities
├── integrations/      # External service integrations
├── monitoring/        # Monitoring and analytics
└── utils/             # General utilities
```

## Tech Stack

- **Database**: SQLAlchemy 2.0, PostgreSQL, Alembic
- **Vector DB**: Chroma
- **LLM**: Multi-provider (Gemini, DeepSeek)
- **Cache**: Redis
- **Integrations**: Slack, Email (SMTP), GitHub API

## Key Components

### Database (`database/`)
- PostgreSQL connection management
- SQLAlchemy models for all entities
- Database migrations (Alembic)
- Query utilities

### Vector DB (`vector_db/`)
- Chroma client wrapper
- Embedding generation
- Collection management
- Semantic search utilities

### LLM (`llm/`)
- Base provider interface
- Gemini provider implementation
- DeepSeek provider implementation
- Provider factory for easy switching
- Prompt templates
- JSON response parsing

### Cache (`cache/`)
- Redis client wrapper
- Caching utilities
- Rate limiting helpers

### Integrations (`integrations/`)
- Slack webhook client
- Email SMTP client
- GitHub API client

### Monitoring (`monitoring/`)
- Metrics collection
- Structured logging
- Analytics aggregation

### Utils (`utils/`)
- Input validation
- Response formatting
- Custom exceptions

## Usage Examples

### Using LLM Provider

```python
from tools.llm.providers.factory import get_llm_provider

llm = get_llm_provider()
response = await llm.generate_json(
    prompt="Classify this ticket...",
    schema={"category": "string", "confidence": "float"}
)
```

### Using Database

```python
from tools.database.postgres import get_db_session
from tools.database.models.ticket import Ticket

async with get_db_session() as session:
    ticket = await session.get(Ticket, ticket_id)
```

### Using Vector DB

```python
from tools.vector_db.chroma_client import get_chroma_client

client = get_chroma_client()
results = await client.search(
    query_text="duplicate charge",
    collection_name="support_cases",
    top_k=5
)
```

## Dependencies

All tools are designed to be imported by agents and services. They handle their own dependencies and configuration via environment variables.

## Configuration

Each tool reads configuration from environment variables. See `.env.example` for all required settings.



