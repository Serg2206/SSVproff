

"""
Pydantic schemas for task-related operations.
"""
from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field, ConfigDict


class TaskBase(BaseModel):
    """Base task schema with common attributes."""
    
    title: str = Field(
        ...,
        min_length=1,
        max_length=200,
        description="Task title"
    )
    description: Optional[str] = Field(
        None,
        description="Task description (optional)"
    )
    is_completed: bool = Field(
        default=False,
        description="Whether the task is completed"
    )


class TaskCreate(TaskBase):
    """Schema for task creation."""
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "title": "Complete project documentation",
                "description": "Write comprehensive API documentation",
                "is_completed": False
            }
        }
    )


class TaskUpdate(BaseModel):
    """Schema for task updates."""
    
    title: Optional[str] = Field(
        None,
        min_length=1,
        max_length=200,
        description="Updated task title"
    )
    description: Optional[str] = Field(
        None,
        description="Updated task description"
    )
    is_completed: Optional[bool] = Field(
        None,
        description="Updated completion status"
    )
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "title": "Complete project documentation",
                "description": "Write comprehensive API and user documentation",
                "is_completed": True
            }
        }
    )


class TaskResponse(TaskBase):
    """Schema for task response."""
    
    id: UUID = Field(..., description="Unique task identifier")
    owner_id: UUID = Field(..., description="ID of the user who owns this task")
    created_at: datetime = Field(..., description="Task creation timestamp")
    updated_at: datetime = Field(..., description="Task last update timestamp")
    
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "title": "Complete project documentation",
                "description": "Write comprehensive API documentation",
                "is_completed": False,
                "owner_id": "123e4567-e89b-12d3-a456-426614174001",
                "created_at": "2024-01-01T00:00:00",
                "updated_at": "2024-01-01T00:00:00"
            }
        }
    )

