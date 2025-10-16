

"""
Task model for example CRUD operations with authentication.

This demonstrates how to create protected resources that require authentication.
"""
import uuid
from datetime import datetime
from sqlalchemy import Boolean, Column, String, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import Index

from app.db.base import Base
from app.models.user import GUID


class Task(Base):
    """
    Task model representing user tasks.
    
    This is an example resource that demonstrates authenticated CRUD operations.
    
    Attributes:
        id: Unique task identifier (UUID)
        title: Task title
        description: Task description (optional)
        is_completed: Whether the task is completed
        owner_id: ID of the user who owns this task
        owner: Relationship to User model
        created_at: Timestamp when task was created
        updated_at: Timestamp when task was last updated
    """
    
    __tablename__ = "tasks"
    
    # Primary key
    id = Column(
        GUID(),
        primary_key=True,
        default=uuid.uuid4,
        index=True,
        doc="Unique task identifier"
    )
    
    # Task fields
    title = Column(
        String(200),
        nullable=False,
        doc="Task title"
    )
    
    description = Column(
        Text,
        nullable=True,
        doc="Task description"
    )
    
    is_completed = Column(
        Boolean,
        default=False,
        nullable=False,
        doc="Whether the task is completed"
    )
    
    # Foreign key to user
    owner_id = Column(
        GUID(),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        doc="ID of the user who owns this task"
    )
    
    # Relationship to User model
    owner = relationship("User", backref="tasks")
    
    # Timestamps
    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
        doc="Timestamp when task was created"
    )
    
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
        doc="Timestamp when task was last updated"
    )
    
    # Indexes for better query performance
    __table_args__ = (
        Index('ix_tasks_owner_completed', 'owner_id', 'is_completed'),
        Index('ix_tasks_owner_created', 'owner_id', 'created_at'),
    )
    
    def __repr__(self) -> str:
        """String representation of Task."""
        return f"<Task(id={self.id}, title={self.title}, owner_id={self.owner_id})>"

