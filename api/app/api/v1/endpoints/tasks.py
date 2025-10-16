

"""
Task endpoints - Example of protected CRUD operations.

This module demonstrates how to create authenticated endpoints
that require JWT token authentication.
"""
from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user
from app.models.user import User
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse
from app.services.task import (
    get_user_tasks,
    get_task_by_id,
    create_task,
    update_task,
    delete_task
)

router = APIRouter()


@router.get("/", response_model=List[TaskResponse])
def list_tasks(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=100, description="Maximum number of records to return"),
    completed: Optional[bool] = Query(None, description="Filter by completion status"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get all tasks for the current user.
    
    This is a protected endpoint that requires authentication.
    
    Args:
        skip: Number of records to skip (pagination)
        limit: Maximum number of records to return (max 100)
        completed: Filter by completion status (optional)
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        List of user's tasks
        
    Example:
        GET /api/v1/tasks?skip=0&limit=10&completed=false
        Headers: Authorization: Bearer <access_token>
        
        Response:
        [
            {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "title": "Complete project",
                "description": "Finish the API",
                "is_completed": false,
                "owner_id": "123e4567-e89b-12d3-a456-426614174001",
                "created_at": "2024-01-01T00:00:00",
                "updated_at": "2024-01-01T00:00:00"
            }
        ]
    """
    tasks = get_user_tasks(db, current_user, skip=skip, limit=limit, completed=completed)
    return tasks


@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_new_task(
    task_data: TaskCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create a new task for the current user.
    
    This is a protected endpoint that requires authentication.
    
    Args:
        task_data: Task creation data
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        Created task
        
    Example:
        POST /api/v1/tasks
        Headers: Authorization: Bearer <access_token>
        {
            "title": "Complete project",
            "description": "Finish the API",
            "is_completed": false
        }
        
        Response:
        {
            "id": "123e4567-e89b-12d3-a456-426614174000",
            "title": "Complete project",
            "description": "Finish the API",
            "is_completed": false,
            "owner_id": "123e4567-e89b-12d3-a456-426614174001",
            "created_at": "2024-01-01T00:00:00",
            "updated_at": "2024-01-01T00:00:00"
        }
    """
    task = create_task(db, task_data, current_user)
    return task


@router.get("/{task_id}", response_model=TaskResponse)
def get_task(
    task_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get a specific task by ID.
    
    This is a protected endpoint that requires authentication.
    Only returns the task if it belongs to the current user.
    
    Args:
        task_id: Task ID
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        Task details
        
    Raises:
        HTTPException 404: If task not found or doesn't belong to user
        
    Example:
        GET /api/v1/tasks/123e4567-e89b-12d3-a456-426614174000
        Headers: Authorization: Bearer <access_token>
        
        Response:
        {
            "id": "123e4567-e89b-12d3-a456-426614174000",
            "title": "Complete project",
            "description": "Finish the API",
            "is_completed": false,
            "owner_id": "123e4567-e89b-12d3-a456-426614174001",
            "created_at": "2024-01-01T00:00:00",
            "updated_at": "2024-01-01T00:00:00"
        }
    """
    task = get_task_by_id(db, task_id, current_user)
    
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    
    return task


@router.put("/{task_id}", response_model=TaskResponse)
def update_existing_task(
    task_id: UUID,
    task_data: TaskUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update a task.
    
    This is a protected endpoint that requires authentication.
    Only allows updating tasks that belong to the current user.
    
    Args:
        task_id: Task ID to update
        task_data: Updated task data
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        Updated task
        
    Raises:
        HTTPException 404: If task not found or doesn't belong to user
        
    Example:
        PUT /api/v1/tasks/123e4567-e89b-12d3-a456-426614174000
        Headers: Authorization: Bearer <access_token>
        {
            "is_completed": true
        }
        
        Response:
        {
            "id": "123e4567-e89b-12d3-a456-426614174000",
            "title": "Complete project",
            "description": "Finish the API",
            "is_completed": true,
            "owner_id": "123e4567-e89b-12d3-a456-426614174001",
            "created_at": "2024-01-01T00:00:00",
            "updated_at": "2024-01-01T00:05:00"
        }
    """
    task = update_task(db, task_id, task_data, current_user)
    
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    
    return task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_existing_task(
    task_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Delete a task.
    
    This is a protected endpoint that requires authentication.
    Only allows deleting tasks that belong to the current user.
    
    Args:
        task_id: Task ID to delete
        current_user: Current authenticated user
        db: Database session
        
    Raises:
        HTTPException 404: If task not found or doesn't belong to user
        
    Example:
        DELETE /api/v1/tasks/123e4567-e89b-12d3-a456-426614174000
        Headers: Authorization: Bearer <access_token>
        
        Response: 204 No Content
    """
    success = delete_task(db, task_id, current_user)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

