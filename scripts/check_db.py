"""Check database status."""
import asyncio
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from tools.database.postgres import engine, get_db_session
from sqlalchemy import text


async def check_database():
    """Check database tables and data."""
    print("=" * 60)
    print("Database Status Check")
    print("=" * 60)
    print()
    
    try:
        # Check tables
        print("1. Checking database tables...")
        async with engine.begin() as conn:
            result = await conn.execute(
                text("""
                    SELECT table_name 
                    FROM information_schema.tables 
                    WHERE table_schema = 'public' 
                    ORDER BY table_name
                """)
            )
            tables = [row[0] for row in result]
            
            if tables:
                print(f"   [OK] Found {len(tables)} tables:")
                for table in tables:
                    print(f"      - {table}")
            else:
                print("   [ERROR] No tables found! Database not initialized.")
                print("   Run: python scripts/setup_db.py")
                return False
        
        print()
        
        # Check data counts
        print("2. Checking data in tables...")
        async for session in get_db_session():
            # Similar Cases
            try:
                result = await session.execute(text("SELECT COUNT(*) FROM similar_cases"))
                cases_count = result.scalar()
                print(f"   Similar Cases: {cases_count}")
            except Exception as e:
                print(f"   Similar Cases: [ERROR] {e}")
                cases_count = 0
            
            # Tickets
            try:
                result = await session.execute(text("SELECT COUNT(*) FROM tickets"))
                tickets_count = result.scalar()
                print(f"   Tickets: {tickets_count}")
            except Exception as e:
                print(f"   Tickets: [ERROR] {e}")
                tickets_count = 0
            
            # Classifications
            try:
                result = await session.execute(text("SELECT COUNT(*) FROM classifications"))
                classifications_count = result.scalar()
                print(f"   Classifications: {classifications_count}")
            except Exception as e:
                print(f"   Classifications: [ERROR] {e}")
                classifications_count = 0
            
            # Knowledge Searches
            try:
                result = await session.execute(text("SELECT COUNT(*) FROM knowledge_searches"))
                knowledge_count = result.scalar()
                print(f"   Knowledge Searches: {knowledge_count}")
            except Exception as e:
                print(f"   Knowledge Searches: [ERROR] {e}")
                knowledge_count = 0
            
            # Sentiment Analysis
            try:
                result = await session.execute(text("SELECT COUNT(*) FROM sentiment_analysis"))
                sentiment_count = result.scalar()
                print(f"   Sentiment Analysis: {sentiment_count}")
            except Exception as e:
                print(f"   Sentiment Analysis: [ERROR] {e}")
                sentiment_count = 0
            
            # Decisions
            try:
                result = await session.execute(text("SELECT COUNT(*) FROM decisions"))
                decisions_count = result.scalar()
                print(f"   Decisions: {decisions_count}")
            except Exception as e:
                print(f"   Decisions: [ERROR] {e}")
                decisions_count = 0
            
            break
        
        print()
        print("=" * 60)
        
        # Summary
        if cases_count == 0:
            print("[WARN] Knowledge base not seeded!")
            print("   Run: python scripts/seed_knowledge_base.py")
        else:
            print(f"[OK] Knowledge base has {cases_count} cases")
        
        if tickets_count > 0:
            print(f"[OK] Database has {tickets_count} tickets")
        
        print("=" * 60)
        
        return True
        
    except Exception as e:
        print()
        print("=" * 60)
        print(f"[ERROR] Database check failed: {e}")
        print("=" * 60)
        import traceback
        traceback.print_exc()
        return False
    finally:
        await engine.dispose()


if __name__ == "__main__":
    success = asyncio.run(check_database())
    sys.exit(0 if success else 1)


