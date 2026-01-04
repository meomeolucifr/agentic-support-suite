"""Check Chroma vector database status."""
import asyncio
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from tools.vector_db.chroma_client import get_collection


async def check_chroma():
    """Check Chroma collection status."""
    print("=" * 60)
    print("Chroma Vector Database Status")
    print("=" * 60)
    print()
    
    try:
        collection = get_collection("support_cases")
        
        # Count documents
        count = collection.count()
        print(f"Documents in Chroma: {count}")
        
        if count == 0:
            print()
            print("[WARN] Chroma database is empty!")
            print("   Run: python scripts/seed_knowledge_base.py")
            return False
        
        # Get sample documents
        print()
        print("Sample documents (first 5):")
        results = collection.get(limit=5)
        
        if results["ids"]:
            for i, doc_id in enumerate(results["ids"][:5], 1):
                metadata = results["metadatas"][i-1] if results["metadatas"] else {}
                category = metadata.get("category", "UNKNOWN")
                subcategory = metadata.get("subcategory", "")
                print(f"  {i}. {doc_id} - {category}/{subcategory}")
        
        print()
        print("=" * 60)
        print(f"[OK] Chroma has {count} cases")
        print("=" * 60)
        
        return True
        
    except Exception as e:
        print()
        print("=" * 60)
        print(f"[ERROR] Chroma check failed: {e}")
        print("=" * 60)
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = asyncio.run(check_chroma())
    sys.exit(0 if success else 1)


