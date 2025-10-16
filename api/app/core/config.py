
"""
Application configuration using Pydantic Settings.

This module provides centralized configuration management for the API,
loading settings from environment variables and .env files.
"""
from functools import lru_cache
from typing import List, Optional
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    
    Attributes:
        PROJECT_NAME: The name of the project
        VERSION: API version
        API_V1_PREFIX: API version 1 prefix path
        DEBUG: Debug mode flag
        BACKEND_CORS_ORIGINS: List of allowed CORS origins
        SECRET_KEY: Secret key for JWT and security
        ACCESS_TOKEN_EXPIRE_MINUTES: JWT token expiration time
    """
    
    # Application
    PROJECT_NAME: str = Field(default="SSVproff API", description="Project name")
    VERSION: str = Field(default="0.1.0", description="API version")
    API_V1_PREFIX: str = Field(default="/api/v1", description="API v1 prefix")
    DEBUG: bool = Field(default=False, description="Debug mode")
    
    # CORS - Use comma-separated string in .env file
    BACKEND_CORS_ORIGINS: List[str] = Field(
        default_factory=lambda: ["http://localhost:3000", "http://localhost:8000"],
        description="Allowed CORS origins"
    )
    
    # Security
    SECRET_KEY: str = Field(
        default="your-secret-key-change-in-production-please-use-strong-random-key",
        description="Secret key for JWT and security",
    )
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(
        default=30,
        description="Access token expiration time in minutes"
    )
    
    # Database
    DATABASE_URL: str = Field(
        ...,
        description="PostgreSQL database connection URL"
    )
    
    # Backblaze B2 (from project context)
    B2_KEY_ID: Optional[str] = Field(default=None, description="Backblaze B2 Key ID")
    B2_APP_KEY: Optional[str] = Field(default=None, description="Backblaze B2 Application Key")
    B2_BUCKET_NAME: Optional[str] = Field(default=None, description="Backblaze B2 Bucket Name")
    
    # DVC
    DVC_REMOTE_URL: Optional[str] = Field(default=None, description="DVC remote storage URL")
    
    # Logging
    LOG_LEVEL: str = Field(default="INFO", description="Logging level")
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="allow",
        env_parse_none_str="null",
    )
    
    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def parse_cors_origins(cls, v):
        """
        Parse CORS origins from comma-separated string or list.
        
        Args:
            v: CORS origins as string (comma-separated) or list
            
        Returns:
            List of CORS origin strings
        """
        if isinstance(v, str) and not v.startswith('['):
            return [origin.strip() for origin in v.split(",")]
        if isinstance(v, list):
            return v
        return v


@lru_cache
def get_settings() -> Settings:
    """
    Get cached application settings.
    
    This function uses LRU cache to ensure settings are loaded only once
    and reused throughout the application lifecycle.
    
    Returns:
        Settings: Application settings instance
        
    Example:
        >>> from app.core.config import get_settings
        >>> settings = get_settings()
        >>> print(settings.PROJECT_NAME)
        'SSVproff API'
    """
    return Settings()


# Convenience instance for direct import
settings = get_settings()
