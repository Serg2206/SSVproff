
"""
User model for authentication and user management.
"""
import uuid
from datetime import datetime
from sqlalchemy import Boolean, Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Index
from sqlalchemy.types import TypeDecorator, CHAR

from app.db.base import Base


class GUID(TypeDecorator):
    """
    Platform-independent GUID type.
    
    Uses PostgreSQL's UUID type, otherwise uses CHAR(36) for SQLite.
    """
    impl = CHAR
    cache_ok = True
    
    def load_dialect_impl(self, dialect):
        if dialect.name == 'postgresql':
            return dialect.type_descriptor(UUID(as_uuid=True))
        else:
            return dialect.type_descriptor(CHAR(36))
    
    def process_bind_param(self, value, dialect):
        if value is None:
            return value
        elif dialect.name == 'postgresql':
            return str(value) if isinstance(value, uuid.UUID) else value
        else:
            return str(value) if isinstance(value, uuid.UUID) else value
    
    def process_result_value(self, value, dialect):
        if value is None:
            return value
        else:
            return uuid.UUID(value) if not isinstance(value, uuid.UUID) else value


class User(Base):
    """
    User model representing application users.
    
    Attributes:
        id: Unique user identifier (UUID)
        email: User's email address (unique, indexed)
        username: User's username (unique, indexed)
        hashed_password: Bcrypt hashed password
        is_active: Whether the user account is active
        is_superuser: Whether the user has superuser privileges
        created_at: Timestamp when user was created
        updated_at: Timestamp when user was last updated
    """
    
    __tablename__ = "users"
    
    # Primary key
    id = Column(
        GUID(),
        primary_key=True,
        default=uuid.uuid4,
        index=True,
        doc="Unique user identifier"
    )
    
    # Authentication fields
    email = Column(
        String(255),
        unique=True,
        nullable=False,
        index=True,
        doc="User's email address"
    )
    
    username = Column(
        String(50),
        unique=True,
        nullable=False,
        index=True,
        doc="User's username"
    )
    
    hashed_password = Column(
        String(255),
        nullable=False,
        doc="Bcrypt hashed password"
    )
    
    # Status fields
    is_active = Column(
        Boolean,
        default=True,
        nullable=False,
        doc="Whether the user account is active"
    )
    
    is_superuser = Column(
        Boolean,
        default=False,
        nullable=False,
        doc="Whether the user has superuser privileges"
    )
    
    # Timestamps
    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
        doc="Timestamp when user was created"
    )
    
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
        doc="Timestamp when user was last updated"
    )
    
    # Composite indexes for better query performance
    __table_args__ = (
        Index('ix_users_email_active', 'email', 'is_active'),
        Index('ix_users_username_active', 'username', 'is_active'),
    )
    
    def __repr__(self) -> str:
        """String representation of User."""
        return f"<User(id={self.id}, email={self.email}, username={self.username})>"
