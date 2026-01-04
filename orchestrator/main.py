"""Orchestrator FastAPI application."""
import sys
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
project_root = Path(__file__).parent.parent
env_path = project_root / ".env"
if env_path.exists():
    load_dotenv(env_path)

# Add project root to path
sys.path.insert(0, str(project_root))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from orchestrator.app.api.routes import router
from orchestrator.app.api.health import router as health_router
from tools.monitoring.logger import setup_logging

# Setup logging
setup_logging()

app = FastAPI(
    title="Orchestrator Service",
    description="Master coordinator for multi-agent support system",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(router, prefix="/api", tags=["tickets"])
app.include_router(health_router, prefix="/api", tags=["health"])


@app.get("/")
async def root():
    """Root endpoint."""
    return {"service": "orchestrator", "status": "running"}


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", "8000"))
    uvicorn.run(app, host="0.0.0.0", port=port)

