# Architecture Documentation

## System Overview

The AI Multi-Agent Customer Support System is a microservices-based architecture where specialized AI agents work together to process and resolve customer support tickets.

## Architecture Diagram

```
┌─────────────┐
│   Client    │
│  (Customer) │
└──────┬──────┘
       │
       ▼
┌─────────────────┐
│  Orchestrator   │ ◄─── Master Coordinator
│    Service      │
└──────┬──────────┘
       │
       ├──► Router Agent ──────► Classifies tickets
       │
       ├──► Knowledge Agent ───► Searches solutions
       │
       ├──► Sentiment Agent ───► Analyzes emotion
       │
       └──► Decision Agent ────► Makes final decision
       
       │
       ▼
┌─────────────────────────────────┐
│      Shared Infrastructure       │
├─────────────────────────────────┤
│  PostgreSQL  │  Chroma  │ Redis │
│  (Relational)│ (Vector) │(Cache)│
└─────────────────────────────────┘
```

## Components

### Orchestrator Service

**Purpose**: Master coordinator that manages the ticket processing workflow.

**Responsibilities**:
- Receives ticket submissions
- Coordinates agent calls in sequence
- Manages workflow state
- Handles errors and retries
- Executes decisions (auto-resolve or escalate)

**Technology**: FastAPI, Python 3.11+

### Router Agent

**Purpose**: Classifies incoming tickets into categories.

**Input**: Ticket text
**Output**: Category, subcategory, confidence score

**Categories**:
- BILLING
- TECHNICAL
- BUG
- FEATURE_REQUEST
- ACCOUNT
- SHIPPING
- SPAM
- OTHER

**Technology**: FastAPI, LLM (Gemini/DeepSeek)

### Knowledge Agent

**Purpose**: Searches knowledge base for similar cases and solutions.

**Process**:
1. Converts ticket to embedding
2. Searches Chroma vector database
3. Retrieves similar cases
4. Uses LLM to adapt solutions

**Technology**: FastAPI, Chroma, LLM

### Sentiment Agent

**Purpose**: Analyzes customer sentiment and detects churn risk.

**Output**:
- Sentiment score (0.0 - 1.0)
- Emotional level (CALM, NEUTRAL, UPSET, ANGRY)
- Churn risk flag
- Human intervention requirement

**Technology**: FastAPI, LLM or HuggingFace Transformers

### Decision Engine Agent

**Purpose**: Synthesizes all signals and makes final decision.

**Decision Types**:
- AUTO_RESOLVE - Bot can handle
- ESCALATE_TO_HUMAN - Needs human agent
- ESCALATE_TO_MANAGER - High priority/churn risk

**Decision Logic**:
- Hard rules (sentiment >= 0.85 → escalate)
- LLM-assisted reasoning for nuanced cases
- Context building for human agents

**Technology**: FastAPI, Decision Rules Engine

## Data Flow

1. **Ticket Submission**: Customer submits ticket via API
2. **Orchestrator**: Creates ticket record, starts workflow
3. **Router Agent**: Classifies ticket → saves classification
4. **Knowledge Agent**: Searches for solutions → saves search results
5. **Sentiment Agent**: Analyzes sentiment → saves sentiment data
6. **Decision Agent**: Makes decision → saves decision with context
7. **Execution**: 
   - If AUTO_RESOLVE: Send solution to customer
   - If ESCALATE: Notify support team (Slack/Email)

## Data Storage

### PostgreSQL

Stores relational data:
- Tickets
- Classifications
- Knowledge searches
- Sentiment analysis
- Decisions
- Similar cases metadata

### Chroma Vector Database

Stores embeddings for semantic search:
- Historical case texts
- Embeddings for similarity search
- Metadata (category, resolution, satisfaction)

### Redis

Caching layer:
- FAQ caching
- Rate limiting
- Session data

## Communication Patterns

### Inter-Service Communication

- **Protocol**: HTTP REST APIs
- **Format**: JSON
- **Timeout**: 30 seconds per agent call
- **Retry**: Exponential backoff (3 retries)

### Error Handling

- Retry logic with exponential backoff
- Fallback strategies
- Error logging and monitoring
- Graceful degradation

## Scalability

### Horizontal Scaling

Each agent can be scaled independently:
- Router Agent: Stateless, easy to scale
- Knowledge Agent: Stateless, can scale
- Sentiment Agent: Stateless, can scale
- Decision Agent: Stateless, can scale

### Database Scaling

- PostgreSQL: Read replicas for queries
- Chroma: Can be scaled horizontally
- Redis: Cluster mode for high availability

## Security

- Environment-based configuration
- No hardcoded secrets
- Internal Docker network for agent communication
- API authentication (can be added)
- Rate limiting (can be added)

## Monitoring

- Health check endpoints on all services
- Metrics collection (processing times, success rates)
- Structured logging
- Agent status monitoring

## Performance Targets

- **Total Processing Time**: < 10 seconds per ticket
- **Router Agent**: ~2 seconds
- **Knowledge Agent**: ~3 seconds
- **Sentiment Agent**: ~1 second
- **Decision Agent**: ~2 seconds

## Future Enhancements

- Message queue (RabbitMQ/Kafka) for async processing
- GraphQL API
- WebSocket for real-time updates
- Advanced analytics and reporting
- Multi-tenant support
- A/B testing for decision logic



