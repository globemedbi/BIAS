"""
BIAS Standard FastAPI App Factory
ALL services MUST use this to create their FastAPI application.
No direct FastAPI() instantiation allowed in any service.
"""
import logging
import os
import time
from typing import Optional

import structlog
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

logger = structlog.get_logger()


def create_app(
    service_name: str,
    version: str = "1.0.0",
    description: str = "",
) -> FastAPI:
    """
    Creates a standardized BIAS FastAPI application.

    Args:
        service_name: The BIAS service name (e.g. ORCHESTRATOR)
        version: Service version string
        description: Short service description

    Returns:
        Configured FastAPI application instance
    """
    app = FastAPI(
        title=f"BIAS - {service_name}",
        version=version,
        description=description,
        docs_url="/docs",
        redoc_url="/redoc",
    )

    # Standard CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Standard request logging middleware
    @app.middleware("http")
    async def log_requests(request: Request, call_next):  # type: ignore
        start_time = time.time()
        response = await call_next(request)
        duration_ms = (time.time() - start_time) * 1000
        logger.info(
            "request_handled",
            service=service_name,
            method=request.method,
            path=request.url.path,
            status_code=response.status_code,
            duration_ms=round(duration_ms, 2),
        )
        return response

    # Standard exception handler
    @app.exception_handler(Exception)
    async def global_exception_handler(
        request: Request, exc: Exception
    ) -> JSONResponse:
        logger.error(
            "unhandled_exception",
            service=service_name,
            path=request.url.path,
            error=str(exc),
        )
        return JSONResponse(
            status_code=500,
            content={
                "status": "FAILED",
                "service": service_name,
                "errors": [
                    {
                        "error_code": "INTERNAL_SERVER_ERROR",
                        "message": "An unexpected error occurred",
                    }
                ],
            },
        )

    # Standard health endpoint
    @app.get("/health", tags=["Health"])
    async def health() -> dict:
        return {
            "service": service_name,
            "status": "HEALTHY",
            "version": version,
            "environment": os.getenv("ENVIRONMENT", "development"),
        }

    return app
