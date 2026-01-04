# Vector Database Tools

## Purpose

Chroma vector database client wrapper for semantic search and embedding management.

## Structure

```
vector_db/
├── chroma_client.py    # Chroma client wrapper
├── embeddings.py       # Embedding generation utilities
└── collections.py      # Collection management
```

## Tech Stack

- **Vector DB**: Chroma
- **Embeddings**: Chroma's default embedding models or custom

## Key Components

### ChromaClient
- Connection management
- Collection operations
- Vector search
- Document management

### Embeddings
- Text to vector conversion
- Batch embedding generation
- Custom embedding models support

### Collections
- Collection creation and management
- Metadata handling
- Index management

## Usage Examples

### Getting Client

```python
from tools.vector_db.chroma_client import get_chroma_client

client = get_chroma_client()
```

### Searching Similar Cases

```python
results = await client.search(
    query_text="duplicate charge refund",
    collection_name="support_cases",
    top_k=5,
    filter={"category": "BILLING"}
)
```

### Adding Documents

```python
await client.add_documents(
    collection_name="support_cases",
    documents=["Case text here..."],
    metadatas=[{"case_id": "CASE_123", "category": "BILLING"}],
    ids=["CASE_123"]
)
```

## Configuration

- `CHROMA_HOST` - Chroma server host
- `CHROMA_PORT` - Chroma server port
- `CHROMA_COLLECTION_NAME` - Default collection name



