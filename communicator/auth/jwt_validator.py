"""
JWT validation for the Communicator service.
"""
import os
from typing import Dict, Optional

from shared.communication_layer.logger import get_logger

logger = get_logger("COMMUNICATOR")

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "change-me")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")


def validate_token(token: str) -> Optional[Dict]:
    """
    Validates a JWT token and returns the decoded payload.

    Returns None if the token is invalid or expired.
    Never logs the token value.
    """
    try:
        from jose import JWTError, jwt

        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        return payload
    except Exception as e:
        logger.warning("jwt_validation_failed", error=type(e).__name__)
        return None


def extract_bearer_token(authorization_header: Optional[str]) -> Optional[str]:
    """Extracts the token from a 'Bearer <token>' Authorization header."""
    if not authorization_header:
        return None
    parts = authorization_header.split(" ")
    if len(parts) != 2 or parts[0].lower() != "bearer":
        return None
    return parts[1]
