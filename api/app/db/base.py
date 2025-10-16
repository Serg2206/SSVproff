
"""
Database base class and model imports.

This module provides the declarative base for SQLAlchemy models
and imports all models for Alembic migrations.
"""
from sqlalchemy.ext.declarative import declarative_base

# Create the declarative base
Base = declarative_base()

# Import all models here for Alembic to detect them
# This ensures migrations include all tables
from app.models.user import User  # noqa: F401, E402

__all__ = ["Base"]
