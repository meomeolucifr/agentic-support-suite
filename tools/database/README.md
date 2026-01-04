# Database Tools

## Purpose

Database utilities for PostgreSQL connection management, SQLAlchemy models, and database migrations.

## Structure

```
database/
├── postgres.py           # PostgreSQL connection & session management
├── models/               # SQLAlchemy models
│   ├── ticket.py         # Ticket model
│   ├── classification.py # Classification model
│   ├── knowledge_search.py # Knowledge search model
│   ├── sentiment.py      # Sentiment model
│   ├── decision.py       # Decision model
│   └── similar_case.py   # Similar case model
└── migrations/           # Alembic migrations
```

## Tech Stack

- **ORM**: SQLAlchemy 2.0
- **Database**: PostgreSQL 15+
- **Migrations**: Alembic
- **Async**: asyncpg

## Key Components

### Database Connection
- Async session management
- Connection pooling
- Transaction handling

### Models
- **Ticket**: Core ticket entity
- **Classification**: Router agent results
- **KnowledgeSearch**: Knowledge agent results
- **Sentiment**: Sentiment analysis results
- **Decision**: Decision engine results
- **SimilarCase**: Historical cases for vector search

## Usage Examples

### Getting Database Session

```python
from tools.database.postgres import get_db_session

async with get_db_session() as session:
    # Use session for queries
    result = await session.execute(select(Ticket))
```

### Using Models

```python
from tools.database.models.ticket import Ticket
from tools.database.postgres import get_db_session

async with get_db_session() as session:
    ticket = Ticket(
        customer_id="CUST_123",
        subject="Issue with order",
        body="I need help..."
    )
    session.add(ticket)
    await session.commit()
```

## Configuration

- `POSTGRES_HOST` - Database host
- `POSTGRES_PORT` - Database port
- `POSTGRES_DB` - Database name
- `POSTGRES_USER` - Database user
- `POSTGRES_PASSWORD` - Database password

## Migrations

Run migrations with Alembic:

```bash
alembic upgrade head
```

Create new migration:

```bash
alembic revision --autogenerate -m "description"
```



