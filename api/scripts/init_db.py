
#!/usr/bin/env python3
"""
Database initialization script.

This script initializes the database by running migrations
and optionally creating a test user.
"""
import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy.orm import Session
from app.db.session import engine, SessionLocal
from app.db.base import Base
from app.models.user import User
from app.core.security import get_password_hash


def init_db() -> None:
    """Initialize database tables."""
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("✓ Database tables created successfully!")


def create_test_user(db: Session) -> None:
    """Create a test user for development."""
    # Check if test user already exists
    existing_user = db.query(User).filter(User.email == "test@example.com").first()
    
    if existing_user:
        print("✓ Test user already exists (test@example.com)")
        return
    
    print("Creating test user...")
    test_user = User(
        email="test@example.com",
        username="testuser",
        hashed_password=get_password_hash("testpassword123"),
        is_active=True,
        is_superuser=False,
    )
    
    db.add(test_user)
    db.commit()
    
    print("✓ Test user created successfully!")
    print("  Email: test@example.com")
    print("  Password: testpassword123")


def create_superuser(db: Session) -> None:
    """Create a superuser for administration."""
    # Check if superuser already exists
    existing_user = db.query(User).filter(User.email == "admin@example.com").first()
    
    if existing_user:
        print("✓ Superuser already exists (admin@example.com)")
        return
    
    print("Creating superuser...")
    superuser = User(
        email="admin@example.com",
        username="admin",
        hashed_password=get_password_hash("admin123"),
        is_active=True,
        is_superuser=True,
    )
    
    db.add(superuser)
    db.commit()
    
    print("✓ Superuser created successfully!")
    print("  Email: admin@example.com")
    print("  Password: admin123")
    print("  ⚠️  CHANGE THIS PASSWORD IN PRODUCTION!")


def main() -> None:
    """Main function."""
    print("=" * 60)
    print("SSVproff Database Initialization")
    print("=" * 60)
    
    # Initialize database tables
    init_db()
    
    # Create test users
    db = SessionLocal()
    try:
        create_test_user(db)
        create_superuser(db)
    finally:
        db.close()
    
    print("=" * 60)
    print("Database initialization completed successfully!")
    print("=" * 60)
    print("\nNote: This script creates tables directly.")
    print("For production, use Alembic migrations:")
    print("  alembic upgrade head")


if __name__ == "__main__":
    main()

