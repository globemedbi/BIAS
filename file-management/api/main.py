"""
BIAS FILE_MANAGEMENT — FastAPI Application Entry Point
Port: 8002
Owner: Backend Dev
"""
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "../../"))

from shared.communication_layer.app_factory import create_app

from api.routes import process_routes

app = create_app(
    service_name="FILE_MANAGEMENT",
    version="1.0.0",
    description="Document Pipeline — OCR → Anonymize → Translate",
)

app.include_router(process_routes.router, prefix="/api/v1", tags=["Processing"])
