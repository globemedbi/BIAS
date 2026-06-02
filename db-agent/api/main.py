"""
BIAS DB_AGENT — FastAPI Application Entry Point
Port: 8003  |  Owner: DB Specialist
The ONLY service in BIAS that is allowed to touch any database.
"""

# os provides path utilities needed to locate the shared package
import os

# sys.path manipulation lets Python find the shared/ package outside this service directory
import sys

# adds the BIAS project root (two directories up from api/) to Python's import search path
# without this, "from shared.xxx import yyy" would fail with ModuleNotFoundError
sys.path.append(os.path.join(os.path.dirname(__file__), "../../"))

# imports the shared FastAPI factory — all BIAS services use this instead of FastAPI() directly
# it pre-configures CORS, health checks, structured logging middleware, and error handlers
from shared.communication_layer.app_factory import create_app

# imports every route module — each module defines an APIRouter with its endpoints
from api.routes import claims_routes     # /claims/store, /claims/history
from api.routes import auth_routes       # /authorization/fetch
from api.routes import query_routes      # /query/nl
from api.routes import log_routes        # /logs/audit
from api.routes import registry_routes   # /registry/save, /registry/load

# generic Oracle procedure endpoint — Layer 1 of the 4-layer architecture
# a single endpoint can invoke any Oracle stored procedure by name
from api import routes as procedure_routes   # /execute-procedure

# creates the FastAPI application instance using the shared factory
app = create_app(
    # the service name stamped into every log line and health check response
    service_name="DB_AGENT",
    # the API version returned in response headers and the /docs UI
    version="1.0.0",
    # a description shown in the auto-generated Swagger UI at /docs
    description="Data Domain — the ONLY service that touches any database",
)

# mounts the claims router — all functions in claims_routes.py become /claims/...
app.include_router(claims_routes.router, prefix="/claims", tags=["Claims Data"])

# mounts the authorization router — all functions become /authorization/...
app.include_router(auth_routes.router, prefix="/authorization", tags=["Authorization"])

# mounts the NL2SQL query router — all functions become /query/...
app.include_router(query_routes.router, prefix="/query", tags=["NL2SQL"])

# mounts the audit log router — all functions become /logs/...
app.include_router(log_routes.router, prefix="/logs", tags=["Audit Logs"])

# mounts the registry router — all functions become /registry/...
# this pair of endpoints lets the Orchestrator persist and restore its service registry
app.include_router(registry_routes.router, prefix="/registry", tags=["Service Registry"])

# mounts the generic Oracle procedure router — the single endpoint becomes /execute-procedure
# any Oracle PL/SQL package procedure can be called without touching this file again
app.include_router(procedure_routes.router, tags=["Oracle Procedures"])
