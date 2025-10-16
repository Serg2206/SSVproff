
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, field_validator
from typing import Optional, List, Union
import os
from pathlib import Path


class Settings(BaseSettings):
    """
    Application settings using Pydantic BaseSettings
    Automatically loads from environment variables or .env file
    """
    
    # Application
    APP_NAME: str = "SSVproff API"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = Field(default=False)
    
    # Database
    DATABASE_URL: str = Field(
        default="sqlite:///./ssvproff.db",
        description="Database connection URL"
    )
    
    # Security
    SECRET_KEY: str = Field(
        default="your-secret-key-change-in-production",
        description="Secret key for JWT token generation"
    )
    ALGORITHM: str = Field(default="HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=30)
    
    # CORS
    CORS_ORIGINS: Union[List[str], str] = Field(
        default=["http://localhost:3000", "http://localhost:8000"],
        description="Allowed CORS origins"
    )
    
    @field_validator('CORS_ORIGINS', mode='before')
    @classmethod
    def parse_cors_origins(cls, v):
        """Parse CORS origins from comma-separated string or list"""
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(',')]
        return v
    
    # API
    API_V1_PREFIX: str = "/api/v1"
    
    # File Storage
    UPLOAD_DIR: str = Field(
        default="./uploads",
        description="Directory for file uploads"
    )
    MAX_UPLOAD_SIZE: int = Field(
        default=100 * 1024 * 1024,  # 100MB
        description="Maximum file upload size in bytes"
    )
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="allow"
    )


# Create settings instance
settings = Settings()

# Ensure upload directory exists
Path(settings.UPLOAD_DIR).mkdir(parents=True, exist_ok=True)
