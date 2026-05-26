"""
BIAS CHATBOT — FastAPI Application Entry Point
Port: 8006
Owner: Frontend Dev
"""
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "../../"))

from shared.communication_layer.app_factory import create_app

from api.routes import chat_routes, format_routes

app = create_app(
    service_name="CHATBOT",
    version="1.0.0",
    description="User Interface — conversational formatting and intent routing",
)

app.include_router(format_routes.router, prefix="/api/v1", tags=["Formatting"])
app.include_router(chat_routes.router, prefix="/api/v1", tags=["Chat"])
