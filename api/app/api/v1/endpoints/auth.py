
"""
Authentication endpoints.

This module provides REST API endpoints for user authentication
including registration, login, and token management.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin, UserResponse, Token
from app.schemas.auth import RefreshTokenRequest
from app.services.auth import (
    create_user,
    authenticate_user,
    create_tokens_for_user,
    refresh_access_token
)

router = APIRouter()


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    """
    Register a new user.
    
    Args:
        user_data: User registration data (email, username, password)
        db: Database session
        
    Returns:
        Created user information (excluding password)
        
    Raises:
        HTTPException 400: If email or username already exists
        HTTPException 422: If validation fails
        
    Example:
        POST /api/v1/auth/register
        {
            "email": "user@example.com",
            "username": "johndoe",
            "password": "securepassword123"
        }
        
        Response:
        {
            "id": "123e4567-e89b-12d3-a456-426614174000",
            "email": "user@example.com",
            "username": "johndoe",
            "is_active": true,
            "is_superuser": false,
            "created_at": "2024-01-01T00:00:00",
            "updated_at": "2024-01-01T00:00:00"
        }
    """
    user = create_user(db, user_data)
    return user


@router.post("/login", response_model=Token)
def login(
    login_data: UserLogin,
    db: Session = Depends(get_db)
):
    """
    Login with email and password to receive JWT tokens.
    
    Args:
        login_data: User login credentials (email, password)
        db: Database session
        
    Returns:
        JWT access token, refresh token, and token type
        
    Raises:
        HTTPException 401: If credentials are invalid
        HTTPException 400: If user is inactive
        
    Example:
        POST /api/v1/auth/login
        {
            "email": "user@example.com",
            "password": "securepassword123"
        }
        
        Response:
        {
            "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
            "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
            "token_type": "bearer"
        }
    """
    user = authenticate_user(db, login_data)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    
    tokens = create_tokens_for_user(user)
    return tokens


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: User = Depends(get_current_user)
):
    """
    Get current authenticated user information.
    
    This is a protected endpoint that requires a valid JWT token.
    
    Args:
        current_user: Current authenticated user (from JWT token)
        
    Returns:
        Current user information (excluding password)
        
    Raises:
        HTTPException 401: If token is invalid or missing
        
    Example:
        GET /api/v1/auth/me
        Headers: Authorization: Bearer <access_token>
        
        Response:
        {
            "id": "123e4567-e89b-12d3-a456-426614174000",
            "email": "user@example.com",
            "username": "johndoe",
            "is_active": true,
            "is_superuser": false,
            "created_at": "2024-01-01T00:00:00",
            "updated_at": "2024-01-01T00:00:00"
        }
    """
    return current_user


@router.post("/refresh", response_model=Token)
def refresh_token(
    token_data: RefreshTokenRequest,
    db: Session = Depends(get_db)
):
    """
    Get a new access token using a refresh token.
    
    Args:
        token_data: Refresh token
        db: Database session
        
    Returns:
        New JWT access token and token type
        
    Raises:
        HTTPException 401: If refresh token is invalid
        
    Example:
        POST /api/v1/auth/refresh
        {
            "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
        }
        
        Response:
        {
            "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
            "token_type": "bearer"
        }
    """
    tokens = refresh_access_token(db, token_data.refresh_token)
    return tokens
