# Database Migrations

## Purpose

Alembic migrations for database schema changes.

## Usage

### Create Migration

```bash
cd tools/database
alembic revision --autogenerate -m "description"
```

### Apply Migrations

```bash
alembic upgrade head
```

### Rollback Migration

```bash
alembic downgrade -1
```

## Initial Migration

Run initial migration to create all tables:

```bash
alembic upgrade head
```



