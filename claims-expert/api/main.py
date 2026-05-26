"""
BIAS CLAIMS_EXPERT — FastAPI Application Entry Point
Port: 8004
Owner: Claims Dev
"""
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "../../"))

from shared.communication_layer.app_factory import create_app

from api.routes import audit_routes, policy_routes

app = create_app(
    service_name="CLAIMS_EXPERT",
    version="1.0.0",
    description="Business Reasoning — reconciles OCR data against authorization records",
)

app.include_router(audit_routes.router, prefix="/api/v1", tags=["Audit"])
app.include_router(policy_routes.router, prefix="/api/v1", tags=["Policy"])
