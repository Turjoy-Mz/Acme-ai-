"""Custom middleware for authentication and logging."""
from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

async def log_requests(request: Request, call_next):
    """Log incoming requests."""
    start_time = datetime.now()
    
    response = await call_next(request)
    
    duration = (datetime.now() - start_time).total_seconds()
    logger.info(
        f"{request.method} {request.url.path} | "
        f"Status: {response.status_code} | Duration: {duration:.2f}s"
    )
    
    return response

async def api_key_middleware(request: Request, call_next):
    """Validate API key for protected endpoints."""
    from app.config import API_KEY
    
    # Skip authentication for health and docs endpoints
    if request.url.path in ["/", "/health", "/docs", "/openapi.json", "/redoc"]:
        return await call_next(request)
    
    api_key = request.headers.get("X-API-Key")
    if not api_key or api_key != API_KEY:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"detail": "Invalid or missing API key"}
        )
    
    return await call_next(request)
