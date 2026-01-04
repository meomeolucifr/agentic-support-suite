# Agents

## Purpose

This directory contains all individual agent services. Each agent is a microservice that performs a specific task in the ticket processing pipeline.

## Structure

```
agents/
├── router-agent/          # Agent 1: Ticket Classification
├── knowledge-agent/       # Agent 2: Knowledge Base Search
├── sentiment-agent/       # Agent 3: Sentiment Analysis
└── decision-agent/        # Agent 4: Decision Engine
```

## Agent Overview

### Router Agent
**Purpose**: Classifies incoming tickets into categories (BILLING, TECHNICAL, BUG, etc.)

**Tech Stack**: FastAPI, LLM (Gemini/DeepSeek)

**Port**: 8001

### Knowledge Agent
**Purpose**: Searches knowledge base for similar cases and solutions

**Tech Stack**: FastAPI, Chroma Vector DB, LLM

**Port**: 8002

### Sentiment Agent
**Purpose**: Analyzes customer sentiment and detects churn risk

**Tech Stack**: FastAPI, LLM, HuggingFace Transformers

**Port**: 8003

### Decision Agent
**Purpose**: Makes final decision on auto-resolve vs escalation

**Tech Stack**: FastAPI, Decision Rules Engine

**Port**: 8004

## Communication Pattern

All agents follow a consistent API pattern:

1. **Health Check**: `GET /health`
2. **Process Request**: `POST /process`
3. **Metrics**: `GET /metrics`

## Shared Dependencies

All agents depend on:
- Shared tools in `tools/` directory
- PostgreSQL for data persistence
- LLM providers (via tools/llm)
- Redis for caching (optional)

## Deployment

Each agent can be deployed independently as a Docker container or as a separate service. They communicate via HTTP REST APIs.



