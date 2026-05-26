"""
BIAS DB_AGENT — FastAPI Application Entry Point
Port: 8003
Owner: DB Specialist
"""
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "../../"))

from shared.communication_layer.app_factory import create_app

from api.routes import claims_routes, auth_routes, query_routes, log_routes

app = create_app(
    service_name="DB_AGENT",
    version="1.0.0",
    description="Data Domain — the ONLY service that touches any database",
)

app.include_router(claims_routes.router, prefix="/claims", tags=["Claims Data"])
app.include_router(auth_routes.router, prefix="/authorization", tags=["Authorization"])
app.include_router(query_routes.router, prefix="/query", tags=["NL2SQL"])
app.include_router(log_routes.router, prefix="/logs", tags=["Audit Logs"])
