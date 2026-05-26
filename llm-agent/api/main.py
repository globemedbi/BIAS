"""
BIAS LLM_AGENT — FastAPI Application Entry Point
Port: 8005
Owner: AI Dev
"""
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "../../"))

from shared.communication_layer.app_factory import create_app

from api.routes import complete_routes, embed_routes, usage_routes

app = create_app(
    service_name="LLM_AGENT",
    version="1.0.0",
    description="AI Domain — the ONLY service that holds LLM API keys",
)

app.include_router(complete_routes.router, prefix="/api/v1", tags=["Completions"])
app.include_router(embed_routes.router, prefix="/api/v1", tags=["Embeddings"])
app.include_router(usage_routes.router, prefix="/api/v1/usage", tags=["Usage"])
