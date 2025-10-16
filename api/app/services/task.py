

"""
Task service layer.

This module provides business logic for task operations.
Demonstrates how to implement authenticated CRUD operations.
"""
from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.task import Task
from app.models.user import User
from app.schemas.task import TaskCreate, TaskUpdate


def get_user_tasks(
    db: Session,
    user: User,
    skip: int = 0,
    limit: int = 100,
    completed: Optional[bool] = None
) -> List[Task]:
    """
    Get all tasks for a user.
    
    Args:
        db: Database session
        user: Current user
        skip: Number of records to skip (pagination)
        limit: Maximum number of records to return
        completed: Filter by completion status (optional)
        
    Returns:
        List of user's tasks
    """
    query = db.query(Task).filter(Task.owner_id == user.id)
    
    if completed is not None:
        query = query.filter(Task.is_completed == completed)
    
    return query.order_by(Task.created_at.desc()).offset(skip).limit(limit).all()


def get_task_by_id(db: Session, task_id: UUID, user: User) -> Optional[Task]:
    """
    Get a specific task by ID.
    
    Args:
        db: Database session
        task_id: Task ID
        user: Current user
        
    Returns:
        Task if found and owned by user, None otherwise
    """
    return db.query(Task).filter(
        Task.id == task_id,
        Task.owner_id == user.id
    ).first()


def create_task(db: Session, task_data: TaskCreate, user: User) -> Task:
    """
    Create a new task for the user.
    
    Args:
        db: Database session
        task_data: Task creation data
        user: Current user (owner)
        
    Returns:
        Created task
    """
    db_task = Task(
        title=task_data.title,
        description=task_data.description,
        is_completed=task_data.is_completed,
        owner_id=user.id,
    )
    
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    
    return db_task


def update_task(
    db: Session,
    task_id: UUID,
    task_data: TaskUpdate,
    user: User
) -> Optional[Task]:
    """
    Update a task.
    
    Args:
        db: Database session
        task_id: Task ID to update
        task_data: Updated task data
        user: Current user
        
    Returns:
        Updated task if found and owned by user, None otherwise
    """
    db_task = get_task_by_id(db, task_id, user)
    
    if not db_task:
        return None
    
    # Update only provided fields
    update_data = task_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_task, field, value)
    
    db.commit()
    db.refresh(db_task)
    
    return db_task


def delete_task(db: Session, task_id: UUID, user: User) -> bool:
    """
    Delete a task.
    
    Args:
        db: Database session
        task_id: Task ID to delete
        user: Current user
        
    Returns:
        True if task was deleted, False if not found or not owned by user
    """
    db_task = get_task_by_id(db, task_id, user)
    
    if not db_task:
        return False
    
    db.delete(db_task)
    db.commit()
    
    return True

