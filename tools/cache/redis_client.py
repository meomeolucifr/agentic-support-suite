"""Redis cache client."""
import os
import json
from typing import Optional, Any
import redis.asyncio as redis


_redis_client: Optional[redis.Redis] = None


async def get_redis_client() -> redis.Redis:
    """Get Redis client instance."""
    global _redis_client
    
    if _redis_client is not None:
        return _redis_client
    
    redis_host = os.getenv("REDIS_HOST", "localhost")
    redis_port = int(os.getenv("REDIS_PORT", "6379"))
    redis_db = int(os.getenv("REDIS_DB", "0"))
    
    _redis_client = await redis.from_url(
        f"redis://{redis_host}:{redis_port}/{redis_db}",
        decode_responses=True
    )
    
    return _redis_client


async def get(key: str) -> Optional[str]:
    """Get value from cache."""
    client = await get_redis_client()
    return await client.get(key)


async def set(key: str, value: str, ttl: Optional[int] = None):
    """Set value in cache."""
    client = await get_redis_client()
    await client.set(key, value, ex=ttl)


async def get_json(key: str) -> Optional[dict]:
    """Get JSON value from cache."""
    value = await get(key)
    if value:
        return json.loads(value)
    return None


async def set_json(key: str, value: dict, ttl: Optional[int] = None):
    """Set JSON value in cache."""
    await set(key, json.dumps(value), ttl)


async def delete(key: str):
    """Delete key from cache."""
    client = await get_redis_client()
    await client.delete(key)


async def exists(key: str) -> bool:
    """Check if key exists."""
    client = await get_redis_client()
    return await client.exists(key) > 0


async def close_redis():
    """Close Redis connection."""
    global _redis_client
    if _redis_client:
        await _redis_client.close()
        _redis_client = None



