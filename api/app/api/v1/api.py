
"""
API v1 router aggregator.

This module combines all v1 API routers into a single router.
"""
from fastapi import APIRouter

from app.api.v1.endpoints import health, auth, tasks

# Create API v1 router
api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(health.router, tags=["health"])
api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(tasks.router, prefix="/tasks", tags=["tasks"])

# Add more routers as they are created:
# api_router.include_router(users.router, prefix="/users", tags=["users"])
# api_router.include_router(items.router, prefix="/items", tags=["items"])
