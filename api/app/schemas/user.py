
"""
Pydantic schemas for user-related operations.
"""
from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, EmailStr, Field, ConfigDict


class UserBase(BaseModel):
    """Base user schema with common attributes."""
    
    email: EmailStr = Field(..., description="User's email address")
    username: str = Field(
        ...,
        min_length=3,
        max_length=50,
        pattern="^[a-zA-Z0-9_-]+$",
        description="Username (alphanumeric, underscore, hyphen only)"
    )


class UserCreate(UserBase):
    """Schema for user registration."""
    
    password: str = Field(
        ...,
        min_length=8,
        max_length=100,
        description="User password (min 8 characters)"
    )
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "email": "user@example.com",
                "username": "johndoe",
                "password": "securepassword123"
            }
        }
    )


class UserLogin(BaseModel):
    """Schema for user login."""
    
    email: EmailStr = Field(..., description="User's email address")
    password: str = Field(..., description="User password")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "email": "user@example.com",
                "password": "securepassword123"
            }
        }
    )


class UserUpdate(BaseModel):
    """Schema for user updates."""
    
    email: Optional[EmailStr] = Field(None, description="Updated email address")
    username: Optional[str] = Field(
        None,
        min_length=3,
        max_length=50,
        pattern="^[a-zA-Z0-9_-]+$",
        description="Updated username"
    )
    password: Optional[str] = Field(
        None,
        min_length=8,
        max_length=100,
        description="Updated password"
    )


class UserResponse(UserBase):
    """Schema for user response (excludes password)."""
    
    id: UUID = Field(..., description="Unique user identifier")
    is_active: bool = Field(..., description="Whether user is active")
    is_superuser: bool = Field(..., description="Whether user is superuser")
    created_at: datetime = Field(..., description="User creation timestamp")
    updated_at: datetime = Field(..., description="User last update timestamp")
    
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "email": "user@example.com",
                "username": "johndoe",
                "is_active": True,
                "is_superuser": False,
                "created_at": "2024-01-01T00:00:00",
                "updated_at": "2024-01-01T00:00:00"
            }
        }
    )


class Token(BaseModel):
    """Schema for authentication token response."""
    
    access_token: str = Field(..., description="JWT access token")
    refresh_token: Optional[str] = Field(None, description="JWT refresh token")
    token_type: str = Field(default="bearer", description="Token type")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer"
            }
        }
    )


class TokenPayload(BaseModel):
    """Schema for JWT token payload."""
    
    sub: str = Field(..., description="Subject (user ID)")
    exp: datetime = Field(..., description="Expiration time")
    iat: Optional[datetime] = Field(None, description="Issued at time")
    type: str = Field(default="access", description="Token type (access/refresh)")
