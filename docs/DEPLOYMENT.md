# Deployment Guide

## Prerequisites

- Docker and Docker Compose installed
- API keys for LLM providers (Gemini or DeepSeek)
- (Optional) Slack webhook URL for notifications
- (Optional) Email SMTP credentials

## Quick Start

### 1. Clone Repository

```bash
git clone <repository-url>
cd agentic-customer-support-system
```

### 2. Configure Environment

Copy `.env.example` to `.env` and fill in your API keys:

```bash
cp .env.example .env
```

Edit `.env` and set:
- `LLM_PROVIDER=gemini` or `deepseek`
- `GEMINI_API_KEY=your_key` or `DEEPSEEK_API_KEY=your_key`
- Other optional settings (Slack, Email, etc.)

### 3. Start Services

```bash
docker-compose up -d
```

This will start:
- PostgreSQL (port 5432)
- Redis (port 6379)
- Chroma (port 8000)
- Router Agent (port 8001)
- Knowledge Agent (port 8002)
- Sentiment Agent (port 8003)
- Decision Agent (port 8004)
- Orchestrator (port 8000)

### 4. Initialize Database

```bash
docker-compose exec orchestrator python scripts/setup_db.py
```

### 5. Seed Knowledge Base

```bash
docker-compose exec orchestrator python scripts/seed_knowledge_base.py
```

### 6. Verify Installation

```bash
docker-compose exec orchestrator python scripts/test_agents.py
```

## Access Services

- **Orchestrator API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs (FastAPI auto-generated)
- **Frontend**: http://localhost:3000 (if running)

## Production Deployment

### Environment Variables

Set these in your production environment:

```bash
# Database
POSTGRES_HOST=your_postgres_host
POSTGRES_PASSWORD=secure_password

# LLM Provider
LLM_PROVIDER=gemini
GEMINI_API_KEY=your_production_key

# Agent URLs (if using load balancer)
ROUTER_AGENT_URL=http://router-agent:8001
KNOWLEDGE_AGENT_URL=http://knowledge-agent:8002
SENTIMENT_AGENT_URL=http://sentiment-agent:8003
DECISION_AGENT_URL=http://decision-agent:8004
```

### Scaling

Each agent can be scaled independently:

```bash
docker-compose up -d --scale router-agent=3 --scale knowledge-agent=2
```

### Monitoring

- Check logs: `docker-compose logs -f [service-name]`
- Health checks: `curl http://localhost:8000/api/health/detailed`

### Backup

Backup PostgreSQL:

```bash
docker-compose exec postgres pg_dump -U postgres support_system > backup.sql
```

Restore:

```bash
docker-compose exec -T postgres psql -U postgres support_system < backup.sql
```

## Troubleshooting

### Services Not Starting

1. Check logs: `docker-compose logs [service-name]`
2. Verify environment variables are set
3. Check port conflicts
4. Ensure database is healthy: `docker-compose ps`

### Agent Connection Errors

1. Verify agent URLs in orchestrator environment
2. Check network connectivity: `docker-compose exec orchestrator ping router-agent`
3. Verify agent health: `curl http://localhost:8001/api/health`

### Database Connection Issues

1. Verify PostgreSQL is running: `docker-compose ps postgres`
2. Check connection string in environment variables
3. Test connection: `docker-compose exec postgres psql -U postgres -d support_system`

## Updating

To update the system:

```bash
# Pull latest code
git pull

# Rebuild containers
docker-compose build

# Restart services
docker-compose up -d
```

## Security Considerations

1. **API Keys**: Never commit `.env` file to version control
2. **Database**: Use strong passwords in production
3. **Network**: Use internal Docker network for agent communication
4. **HTTPS**: Use reverse proxy (nginx/traefik) for HTTPS in production
5. **Rate Limiting**: Implement rate limiting for public APIs



