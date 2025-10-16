
"""
Dependency injection utilities for API endpoints.

This module provides reusable dependencies for FastAPI endpoints,
such as database sessions, authentication, and common parameters.
"""
from typing import Generator
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.config import get_settings, Settings
from app.core.security import decode_token
from app.db.session import SessionLocal
from app.models.user import User


# OAuth2 scheme for JWT tokens
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login", auto_error=True)


def get_settings_dependency() -> Settings:
    """
    Get application settings as a dependency.
    
    Returns:
        Settings: Application settings instance
        
    Example:
        >>> @app.get("/info")
        >>> def info(settings: Settings = Depends(get_settings_dependency)):
        ...     return {"name": settings.PROJECT_NAME}
    """
    return get_settings()


def get_db() -> Generator[Session, None, None]:
    """
    Get database session as a dependency.
    
    Yields:
        Session: SQLAlchemy database session
        
    Example:
        >>> from sqlalchemy.orm import Session
        >>> @app.get("/items")
        >>> def get_items(db: Session = Depends(get_db)):
        ...     return db.query(Item).all()
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    """
    Get current authenticated user from JWT token.
    
    Args:
        token: JWT token from Authorization header
        db: Database session
        
    Returns:
        User: Current authenticated user
        
    Raises:
        HTTPException: If token is invalid or user not found
        
    Example:
        >>> @app.get("/me")
        >>> def read_users_me(current_user: User = Depends(get_current_user)):
        ...     return current_user
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    # Decode and validate token
    payload = decode_token(token)
    if payload is None:
        raise credentials_exception
    
    user_id: str = payload.get("sub")
    token_type: str = payload.get("type")
    
    if user_id is None or token_type != "access":
        raise credentials_exception
    
    # Get user from database
    user = db.query(User).filter(User.id == user_id).first()
    
    if user is None:
        raise credentials_exception
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    
    return user


async def get_current_active_superuser(
    current_user: User = Depends(get_current_user),
) -> User:
    """
    Get current active superuser.
    
    Args:
        current_user: Current authenticated user
        
    Returns:
        User: Current superuser
        
    Raises:
        HTTPException: If user is not a superuser
        
    Example:
        >>> @app.delete("/users/{user_id}")
        >>> def delete_user(
        ...     user_id: str,
        ...     current_user: User = Depends(get_current_active_superuser)
        ... ):
        ...     # Only superusers can delete users
        ...     pass
    """
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The user doesn't have enough privileges"
        )
    return current_user
