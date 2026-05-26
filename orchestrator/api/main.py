"""
BIAS ORCHESTRATOR — FastAPI Application Entry Point
Port: 8001
Owner: Lead Architect
"""
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "../../"))

from shared.communication_layer.app_factory import create_app

from api.routes import plan_routes, registry_routes, metrics_routes

app = create_app(
    service_name="ORCHESTRATOR",
    version="1.0.0",
    description="Brain / Control Tower — creates Flight Plans and manages service health",
)

app.include_router(plan_routes.router, prefix="/plan", tags=["Flight Plans"])
app.include_router(registry_routes.router, prefix="/registry", tags=["Registry"])
app.include_router(metrics_routes.router, prefix="/metrics", tags=["Metrics"])
