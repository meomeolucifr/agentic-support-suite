# Router Agent

## Purpose

The Router Agent classifies incoming support tickets into categories and subcategories. It's the first agent to process a ticket and determines the routing path.

## Structure

```
router-agent/
├── main.py                    # FastAPI entry point
├── app/
│   ├── agent.py              # RouterAgent class
│   ├── api/
│   │   └── routes.py         # API endpoints
│   └── models/
│       └── classification.py # Classification models
└── requirements.txt
```

## Tech Stack

- **Framework**: FastAPI
- **LLM**: Multi-provider (Gemini/DeepSeek via tools/llm)
- **Validation**: Pydantic v2
- **Logging**: structlog

## Key Components

### RouterAgent Class
- Receives ticket text
- Uses LLM to classify into categories
- Returns category, subcategory, and confidence score

### Categories Supported
- BILLING
- TECHNICAL
- BUG
- FEATURE_REQUEST
- ACCOUNT
- SHIPPING
- SPAM
- OTHER

## Usage Examples

### Starting the Service

```bash
cd agents/router-agent
uvicorn main:app --host 0.0.0.0 --port 8001
```

### Processing a Ticket

```python
POST /process
{
    "ticket_id": "TKT_123",
    "text": "I was charged twice for my order"
}

Response:
{
    "ticket_id": "TKT_123",
    "category": "BILLING",
    "subcategory": "DUPLICATE_CHARGE",
    "confidence": 0.98,
    "reason": "Customer states charged twice"
}
```

## Dependencies

- `tools/llm` - LLM provider abstraction
- `tools/database` - Database models
- PostgreSQL for storing classifications

## Configuration

- `LLM_PROVIDER` - LLM provider to use (gemini/deepseek)
- `GEMINI_API_KEY` or `DEEPSEEK_API_KEY`
- Database connection settings



