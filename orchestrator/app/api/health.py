"""Health check endpoints."""
from fastapi import APIRouter
import httpx
import os

router = APIRouter()


@router.get("/health/detailed")
async def detailed_health_check():
    """Detailed health check including agent status."""
    agents = {
        "router": os.getenv("ROUTER_AGENT_URL", "http://localhost:8001"),
        "knowledge": os.getenv("KNOWLEDGE_AGENT_URL", "http://localhost:8002"),
        "sentiment": os.getenv("SENTIMENT_AGENT_URL", "http://localhost:8003"),
        "decision": os.getenv("DECISION_AGENT_URL", "http://localhost:8004")
    }
    
    agent_status = {}
    for name, url in agents.items():
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get(f"{url}/api/health")
                agent_status[name] = {
                    "status": "healthy" if response.status_code == 200 else "unhealthy",
                    "url": url
                }
        except Exception as e:
            agent_status[name] = {
                "status": "unreachable",
                "error": str(e),
                "url": url
            }
    
    return {
        "orchestrator": "healthy",
        "agents": agent_status
    }



