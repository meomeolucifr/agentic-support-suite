"""Error handling and retry logic."""
import asyncio
from typing import Callable, Any, Optional
from tools.monitoring.logger import get_logger

logger = get_logger(__name__)


async def retry_with_backoff(
    func: Callable,
    max_retries: int = 3,
    initial_delay: float = 1.0,
    backoff_factor: float = 2.0,
    *args,
    **kwargs
) -> Any:
    """
    Retry function with exponential backoff.
    
    Args:
        func: Async function to retry
        max_retries: Maximum number of retries
        initial_delay: Initial delay in seconds
        backoff_factor: Backoff multiplier
        *args: Function arguments
        **kwargs: Function keyword arguments
        
    Returns:
        Function result
        
    Raises:
        Exception: If all retries fail
    """
    delay = initial_delay
    
    for attempt in range(max_retries):
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            if attempt == max_retries - 1:
                logger.error(
                    "Function failed after all retries",
                    function=func.__name__,
                    error=str(e),
                    attempts=max_retries
                )
                raise
            
            logger.warning(
                "Function failed, retrying",
                function=func.__name__,
                error=str(e),
                attempt=attempt + 1,
                delay=delay
            )
            
            await asyncio.sleep(delay)
            delay *= backoff_factor
    
    raise Exception("Retry logic failed unexpectedly")



