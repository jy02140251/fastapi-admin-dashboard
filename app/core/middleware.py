"""Application middleware for logging, CORS, and request tracking."""

import time
import uuid
import logging
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger(__name__)


class RequestTrackingMiddleware(BaseHTTPMiddleware):
    """Add unique request ID and track request duration."""

    async def dispatch(self, request: Request, call_next):
        request_id = str(uuid.uuid4())[:8]
        start_time = time.time()

        request.state.request_id = request_id
        logger.info(
            f"[{request_id}] {request.method} {request.url.path} "
            f"from {request.client.host}"
        )

        response = await call_next(request)

        duration = time.time() - start_time
        response.headers["X-Request-ID"] = request_id
        response.headers["X-Response-Time"] = f"{duration:.4f}s"

        logger.info(
            f"[{request_id}] Completed {response.status_code} in {duration:.4f}s"
        )
        return response


class MaintenanceModeMiddleware(BaseHTTPMiddleware):
    """Block requests when maintenance mode is enabled."""

    ALLOWED_PATHS = {"/health", "/api/auth/login", "/api/settings"}

    def __init__(self, app, enabled: bool = False):
        super().__init__(app)
        self.enabled = enabled

    async def dispatch(self, request: Request, call_next):
        if self.enabled and request.url.path not in self.ALLOWED_PATHS:
            return Response(
                content='{"error": "Service under maintenance"}',
                status_code=503,
                media_type="application/json",
            )
        return await call_next(request)


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Add security headers to all responses."""

    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = (
            "max-age=31536000; includeSubDomains"
        )
        return response