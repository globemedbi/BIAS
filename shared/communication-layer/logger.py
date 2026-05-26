"""
BIAS Standard Logger
ALL services MUST use this logger.
No print() statements. No custom logging setup.
"""
import logging
import os
import sys

import structlog


def get_logger(service_name: str) -> structlog.BoundLogger:
    """
    Returns a structured JSON logger bound to the service name.

    Args:
        service_name: The BIAS service name

    Returns:
        Configured structlog BoundLogger

    Usage:
        from shared.communication_layer.logger import get_logger
        logger = get_logger("CLAIMS_EXPERT")
        logger.info("audit_started", claim_id=claim_id, plan_id=plan_id)
    """
    log_level = os.getenv("LOG_LEVEL", "INFO").upper()

    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.JSONRenderer(),
        ],
        wrapper_class=structlog.make_filtering_bound_logger(
            getattr(logging, log_level)
        ),
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(file=sys.stdout),
    )

    return structlog.get_logger().bind(
        service=service_name,
        environment=os.getenv("ENVIRONMENT", "development"),
    )
