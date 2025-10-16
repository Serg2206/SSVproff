
"""
Database session configuration and management.

This module provides database engine, session factory, and session dependencies
for SQLAlchemy operations with connection pooling.
"""
from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import QueuePool

from app.core.config import settings

# Create database engine with connection pooling
# QueuePool maintains a pool of connections for better performance
engine = create_engine(
    settings.DATABASE_URL,
    poolclass=QueuePool,
    pool_size=5,  # Maximum number of permanent connections
    max_overflow=10,  # Maximum number of temporary connections
    pool_pre_ping=True,  # Verify connections before using them
    pool_recycle=3600,  # Recycle connections after 1 hour
    echo=settings.DEBUG,  # Log SQL statements in debug mode
)

# Create sessionmaker factory
# Sessions created from this factory will use the engine above
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


def get_db() -> Generator[Session, None, None]:
    """
    Dependency that provides a database session.
    
    This function creates a new database session for each request
    and ensures it's properly closed after use.
    
    Yields:
        Session: SQLAlchemy database session
        
    Example:
        >>> from fastapi import Depends
        >>> from sqlalchemy.orm import Session
        >>> 
        >>> @app.get("/users")
        >>> def get_users(db: Session = Depends(get_db)):
        ...     return db.query(User).all()
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db() -> None:
    """
    Initialize database by creating all tables.
    
    Note:
        In production, use Alembic migrations instead.
        This is useful for testing and development.
        
    Example:
        >>> from app.db.session import init_db
        >>> init_db()  # Creates all tables
    """
    from app.db.base import Base
    Base.metadata.create_all(bind=engine)
