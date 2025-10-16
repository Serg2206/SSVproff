
"""
Health check endpoints.

Provides endpoints for monitoring service health and readiness.
"""
from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.core.config import Settings, get_settings

router = APIRouter()


class HealthResponse(BaseModel):
    """Health check response model."""
    status: str
    version: str
    environment: str


class DetailedHealthResponse(BaseModel):
    """Detailed health check response model."""
    status: str
    version: str
    environment: str
    services: dict


@router.get("/health", response_model=HealthResponse)
async def health_check(settings: Settings = Depends(get_settings)):
    """
    Basic health check endpoint.
    
    Returns:
        HealthResponse: Service health status
        
    Example:
        GET /health
        Response: {"status": "ok", "version": "0.1.0", "environment": "development"}
    """
    return HealthResponse(
        status="ok",
        version=settings.VERSION,
        environment="development" if settings.DEBUG else "production",
    )


@router.get("/health/detailed", response_model=DetailedHealthResponse)
async def detailed_health_check(settings: Settings = Depends(get_settings)):
    """
    Detailed health check endpoint with service dependencies status.
    
    Returns:
        DetailedHealthResponse: Detailed service health status
        
    Example:
        GET /health/detailed
        Response: {
            "status": "ok",
            "version": "0.1.0",
            "environment": "development",
            "services": {
                "database": "ok",
                "cache": "ok"
            }
        }
    """
    # TODO: Add actual service health checks
    services_status = {
        "api": "ok",
        # "database": check_database_connection(),
        # "cache": check_cache_connection(),
        # "storage": check_storage_connection(),
    }
    
    overall_status = "ok" if all(s == "ok" for s in services_status.values()) else "degraded"
    
    return DetailedHealthResponse(
        status=overall_status,
        version=settings.VERSION,
        environment="development" if settings.DEBUG else "production",
        services=services_status,
    )


@router.get("/ready")
async def readiness_check():
    """
    Readiness probe endpoint for Kubernetes/container orchestration.
    
    Returns:
        dict: Readiness status
        
    Example:
        GET /ready
        Response: {"ready": true}
    """
    # TODO: Check if all required services are ready
    return {"ready": True}


@router.get("/live")
async def liveness_check():
    """
    Liveness probe endpoint for Kubernetes/container orchestration.
    
    Returns:
        dict: Liveness status
        
    Example:
        GET /live
        Response: {"alive": true}
    """
    return {"alive": True}
