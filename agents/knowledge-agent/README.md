# Knowledge Agent

## Purpose

The Knowledge Agent searches the knowledge base (vector database) for similar cases and solutions. It uses semantic search to find relevant historical cases and adapts solutions to the current ticket.

## Structure

```
knowledge-agent/
├── main.py                    # FastAPI entry point
├── app/
│   ├── agent.py              # KnowledgeAgent class
│   ├── api/
│   │   └── routes.py         # API endpoints
│   ├── search/
│   │   ├── vector_search.py  # Chroma integration
│   │   └── semantic_search.py # Semantic search logic
│   └── models/
│       └── knowledge.py     # Knowledge search models
└── requirements.txt
```

## Tech Stack

- **Framework**: FastAPI
- **Vector DB**: Chroma
- **LLM**: Multi-provider (for solution adaptation)
- **Embeddings**: Chroma's embedding models

## Key Components

### KnowledgeAgent Class
- Receives ticket text and category
- Performs vector search in Chroma
- Retrieves similar cases
- Uses LLM to adapt solutions
- Returns solution with confidence score

### Vector Search
- Converts ticket to embedding
- Searches Chroma collection for similar cases
- Returns top-k matches with similarity scores

## Usage Examples

### Starting the Service

```bash
cd agents/knowledge-agent
uvicorn main:app --host 0.0.0.0 --port 8002
```

### Searching Knowledge Base

```python
POST /process
{
    "ticket_id": "TKT_123",
    "text": "I was charged twice",
    "category": "BILLING"
}

Response:
{
    "ticket_id": "TKT_123",
    "similar_cases_found": 3,
    "top_match_case_id": "CASE_5432",
    "similarity_score": 0.94,
    "solution": "Refund duplicate charge immediately, add $5 credit",
    "confidence": 0.87,
    "solvable_without_escalation": true
}
```

## Dependencies

- `tools/vector_db` - Chroma client wrapper
- `tools/llm` - LLM provider for solution adaptation
- `tools/database` - Database models
- Chroma Vector Database
- PostgreSQL for metadata

## Configuration

- `CHROMA_HOST` - Chroma server host
- `CHROMA_PORT` - Chroma server port
- `LLM_PROVIDER` - LLM provider for solution adaptation
- Database connection settings



