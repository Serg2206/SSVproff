
"""
Database base class.

This module provides the declarative base for SQLAlchemy models.
"""
from sqlalchemy.ext.declarative import declarative_base

# Create the declarative base
Base = declarative_base()

__all__ = ["Base"]
