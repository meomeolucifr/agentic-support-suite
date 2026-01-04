# Utility Scripts

## Purpose

Setup, maintenance, and testing scripts for the support system.

## Structure

```
scripts/
├── setup_db.py           # Database initialization
├── seed_knowledge_base.py # Seed vector DB with cases
├── migrate_db.py         # Run database migrations
└── test_agents.py        # Test agent endpoints
```

## Scripts

### setup_db.py
Initializes the database:
- Creates database if not exists
- Runs migrations
- Sets up initial schema

### seed_knowledge_base.py
Seeds the Chroma vector database:
- Adds sample support cases
- Generates embeddings
- Creates collections

### migrate_db.py
Runs Alembic migrations:
- Applies pending migrations
- Shows migration status

### test_agents.py
Tests all agent endpoints:
- Health checks
- Process requests
- Validates responses

## Usage Examples

### Setup Database

```bash
python scripts/setup_db.py
```

### Seed Knowledge Base

```bash
python scripts/seed_knowledge_base.py
```

### Run Migrations

```bash
python scripts/migrate_db.py
```

### Test Agents

```bash
python scripts/test_agents.py
```

## Dependencies

- Database connection configured
- All services running (for test script)
- Required environment variables set



