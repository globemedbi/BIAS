"""
BIAS Standard Retry Handler
Provides consistent retry logic across all services.
"""
import asyncio
from typing import Any, Callable, Optional, Type

import structlog

logger = structlog.get_logger()


async def with_retry(
    func: Callable,
    max_attempts: int = 3,
    delay_seconds: float = 1.0,
    backoff_multiplier: float = 2.0,
    exceptions: tuple = (Exception,),
    service_name: str = "UNKNOWN",
    operation_name: str = "UNKNOWN",
) -> Any:
    """
    Executes a function with exponential backoff retry.

    Args:
        func: Async callable to retry
        max_attempts: Maximum number of attempts
        delay_seconds: Initial delay between retries
        backoff_multiplier: Multiplier for each retry delay
        exceptions: Exception types that trigger a retry
        service_name: Service name for logging
        operation_name: Operation name for logging

    Returns:
        Result of the function call

    Raises:
        Last exception if all retries exhausted
    """
    last_exception: Optional[Exception] = None
    delay = delay_seconds

    for attempt in range(1, max_attempts + 1):
        try:
            return await func()
        except exceptions as e:
            last_exception = e
            if attempt < max_attempts:
                logger.warning(
                    "retry_attempt",
                    service=service_name,
                    operation=operation_name,
                    attempt=attempt,
                    max_attempts=max_attempts,
                    retry_in_seconds=delay,
                    error=str(e),
                )
                await asyncio.sleep(delay)
                delay *= backoff_multiplier
            else:
                logger.error(
                    "retry_exhausted",
                    service=service_name,
                    operation=operation_name,
                    attempts=max_attempts,
                    error=str(e),
                )

    raise last_exception  # type: ignore
