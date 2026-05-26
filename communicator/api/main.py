"""
BIAS COMMUNICATOR — FastAPI Application Entry Point
Port: 8000
Owner: Backend Dev
"""
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "../../"))

from shared.communication_layer.app_factory import create_app

from api.routes import claims_routes, internal_routes

app = create_app(
    service_name="COMMUNICATOR",
    version="1.0.0",
    description="External Gateway — JWT auth, rate limiting, 202 pattern",
)

app.include_router(claims_routes.router, prefix="/api/v1/claims", tags=["Claims"])
app.include_router(internal_routes.router, prefix="/internal/v1", tags=["Internal"])


@app.get("/api/v1/health", tags=["Health"])
async def external_health() -> dict:
    """External health check endpoint."""
    return {"service": "COMMUNICATOR", "status": "HEALTHY", "version": "1.0.0"}
