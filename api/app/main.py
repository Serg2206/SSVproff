"""
SSVproff API - Main application entry point.

This module initializes and configures the FastAPI application with all
middleware, routers, and event handlers.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from datetime import datetime
import logging

from app.api.v1.api import api_router
from app.core.config import settings

# Create FastAPI application instance
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="API for SSVproff - монорепо с документацией, автоматизацией и заготовками API/Web",
    openapi_url=f"{settings.API_V1_PREFIX}/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API v1 router
app.include_router(api_router, prefix=settings.API_V1_PREFIX)


# Root endpoint - provides basic API information
@app.get("/")
def root():
    """
    Root endpoint returning API information.
    
    Returns:
        dict: API name and version information
    """
    return {
        "name": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "docs": "/docs",
        "redoc": "/redoc",
        "api_v1": settings.API_V1_PREFIX,
    }


# Legacy health endpoint (kept for backward compatibility)
# Prefer using /api/v1/health instead
@app.get("/health")
def health_legacy():
    """
    Legacy health check endpoint.
    
    Note:
        Use /api/v1/health for the current health check endpoint.
        This endpoint is kept for backward compatibility.
    
    Returns:
        dict: Health status
    """
    return {"status": "ok"}


@app.on_event("startup")
async def startup_event():
    """
    Application startup event handler.
    
    Performs initialization tasks when the application starts.
    """
    # TODO: Initialize database connections
    # TODO: Initialize cache connections
    # TODO: Load ML models if any
    pass


@app.on_event("shutdown")
async def shutdown_event():
    """
    Application shutdown event handler.
    
    Performs cleanup tasks when the application shuts down.
    """
    # TODO: Close database connections
    # TODO: Close cache connections
    # TODO: Cleanup resources
    pass
