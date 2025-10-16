
"""
Authentication service layer.

This module provides business logic for user authentication operations
including registration, login, and token management.
"""
from typing import Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.user import User
from app.schemas.user import UserCreate, UserLogin
from app.core.security import (
    verify_password,
    get_password_hash,
    create_access_token,
    create_refresh_token,
    decode_token
)


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    """
    Get user by email address.
    
    Args:
        db: Database session
        email: User's email address
        
    Returns:
        User if found, None otherwise
    """
    return db.query(User).filter(User.email == email).first()


def get_user_by_username(db: Session, username: str) -> Optional[User]:
    """
    Get user by username.
    
    Args:
        db: Database session
        username: User's username
        
    Returns:
        User if found, None otherwise
    """
    return db.query(User).filter(User.username == username).first()


def create_user(db: Session, user_data: UserCreate) -> User:
    """
    Create a new user.
    
    Args:
        db: Database session
        user_data: User creation data
        
    Returns:
        Created user
        
    Raises:
        HTTPException: If email or username already exists
    """
    # Check if email already exists
    if get_user_by_email(db, user_data.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Check if username already exists
    if get_user_by_username(db, user_data.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken"
        )
    
    # Create new user
    hashed_password = get_password_hash(user_data.password)
    db_user = User(
        email=user_data.email,
        username=user_data.username,
        hashed_password=hashed_password,
        is_active=True,
        is_superuser=False,
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user


def authenticate_user(db: Session, login_data: UserLogin) -> Optional[User]:
    """
    Authenticate user with email and password.
    
    Args:
        db: Database session
        login_data: User login credentials
        
    Returns:
        User if authentication successful, None otherwise
    """
    user = get_user_by_email(db, login_data.email)
    
    if not user:
        return None
    
    if not verify_password(login_data.password, user.hashed_password):
        return None
    
    return user


def create_tokens_for_user(user: User) -> dict:
    """
    Create access and refresh tokens for a user.
    
    Args:
        user: User object
        
    Returns:
        Dictionary containing access_token, refresh_token, and token_type
    """
    access_token = create_access_token(data={"sub": str(user.id)})
    refresh_token = create_refresh_token(data={"sub": str(user.id)})
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


def refresh_access_token(db: Session, refresh_token: str) -> dict:
    """
    Create new access token from refresh token.
    
    Args:
        db: Database session
        refresh_token: Valid refresh token
        
    Returns:
        Dictionary containing new access_token and token_type
        
    Raises:
        HTTPException: If refresh token is invalid or user not found
    """
    # Decode and validate refresh token
    payload = decode_token(refresh_token)
    
    if payload is None or payload.get("type") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )
    
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )
    
    # Get user from database
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or inactive"
        )
    
    # Create new access token
    access_token = create_access_token(data={"sub": str(user.id)})
    
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
