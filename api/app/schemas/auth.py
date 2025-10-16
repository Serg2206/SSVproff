
"""
Pydantic schemas for authentication operations.
"""
from pydantic import BaseModel, Field, ConfigDict


class RefreshTokenRequest(BaseModel):
    """Schema for refresh token request."""
    
    refresh_token: str = Field(..., description="Refresh token to exchange for new access token")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
            }
        }
    )
