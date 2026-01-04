"""Database setup script."""
import asyncio
import sys
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from tools.database.postgres import init_db, engine, Base
# Import all models to register them with Base
from tools.database.models import (
    Ticket, Classification, KnowledgeSearch, 
    Sentiment, Decision, SimilarCase
)


async def setup_database():
    """Initialize database and create all tables."""
    print("=" * 60)
    print("Database Setup")
    print("=" * 60)
    print()
    
    try:
        # Import all models to ensure they're registered
        print("Registering database models...")
        print(f"  - Tickets table")
        print(f"  - Classifications table")
        print(f"  - Knowledge Searches table")
        print(f"  - Sentiment Analysis table")
        print(f"  - Decisions table")
        print(f"  - Similar Cases table")
        print()
        
        # Create all tables using init_db function
        print("Creating database tables...")
        await init_db()
        
        print()
        print("=" * 60)
        print("[OK] Database initialized successfully!")
        print("[OK] All tables created")
        print("=" * 60)
        
    except Exception as e:
        print()
        print("=" * 60)
        print(f"[ERROR] Error initializing database: {e}")
        print("=" * 60)
        import traceback
        traceback.print_exc()
        sys.exit(1)
    finally:
        await engine.dispose()


if __name__ == "__main__":
    asyncio.run(setup_database())

