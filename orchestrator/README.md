# Orchestrator Service

## Purpose

The Orchestrator is the master coordinator service that manages the entire ticket processing workflow. It coordinates all four agents, handles error recovery, and manages the ticket lifecycle.

## Structure

```
orchestrator/
├── main.py                 # FastAPI entry point
├── app/
│   ├── api/               # API routes
│   │   ├── routes.py      # Ticket submission endpoints
│   │   └── health.py      # Health check endpoints
│   ├── core/              # Core orchestration logic
│   │   ├── orchestrator.py # Main coordination logic
│   │   ├── workflow.py    # Workflow state machine
│   │   └── error_handler.py # Error handling & retries
│   └── models/            # Data models
│       └── ticket.py      # Ticket data models
└── requirements.txt
```

## Tech Stack

- **Framework**: FastAPI
- **Language**: Python 3.11+
- **HTTP Client**: httpx (async)
- **Validation**: Pydantic v2
- **Logging**: structlog

## Key Components

### Orchestrator Class
- Coordinates agent calls in sequence
- Manages workflow state
- Handles retries and error recovery
- Aggregates agent responses

### Workflow State Machine
- NEW → ROUTING → KNOWLEDGE_SEARCH → SENTIMENT_ANALYSIS → DECISION → RESOLVED/ESCALATED
- Tracks ticket status throughout processing

### Error Handler
- Retry logic for failed agent calls
- Fallback strategies
- Error logging and monitoring

## Usage Examples

### Starting the Service

```bash
cd orchestrator
uvicorn main:app --host 0.0.0.0 --port 8000
```

### Submitting a Ticket

```python
import httpx

async with httpx.AsyncClient() as client:
    response = await client.post(
        "http://localhost:8000/api/tickets",
        json={
            "customer_id": "CUST_123",
            "subject": "I was charged twice",
            "body": "I noticed two charges on my account..."
        }
    )
```

## Dependencies

- Router Agent Service (port 8001)
- Knowledge Agent Service (port 8002)
- Sentiment Agent Service (port 8003)
- Decision Agent Service (port 8004)
- PostgreSQL Database
- Redis Cache

## Configuration

Required environment variables:
- `ROUTER_AGENT_URL` - URL of router agent service
- `KNOWLEDGE_AGENT_URL` - URL of knowledge agent service
- `SENTIMENT_AGENT_URL` - URL of sentiment agent service
- `DECISION_AGENT_URL` - URL of decision agent service
- `POSTGRES_HOST`, `POSTGRES_PORT`, `POSTGRES_DB`, etc.
- `REDIS_HOST`, `REDIS_PORT`



