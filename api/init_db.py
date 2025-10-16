
#!/usr/bin/env python3
"""
Database initialization script for SSVproff

This script initializes the database by creating all tables
and optionally creating a default admin user.
"""

import sys
import os
from pathlib import Path

# Add the parent directory to the path so we can import from app
sys.path.insert(0, str(Path(__file__).parent))

from app.database import init_db, SessionLocal
from app.models import User
from app.auth import get_password_hash


def create_admin_user(db):
    """Create a default admin user if it doesn't exist"""
    admin = db.query(User).filter(User.username == "admin").first()
    
    if not admin:
        admin = User(
            username="admin",
            email="admin@example.com",
            hashed_password=get_password_hash("admin123"),
            is_active=True,
            is_superuser=True
        )
        db.add(admin)
        db.commit()
        print("✓ Default admin user created")
        print("  Username: admin")
        print("  Password: admin123")
        print("  ⚠️  Please change the password immediately!")
    else:
        print("✓ Admin user already exists")


def main():
    """Main function"""
    print("=" * 50)
    print("SSVproff Database Initialization")
    print("=" * 50)
    
    try:
        # Initialize database (create tables)
        print("\n1. Creating database tables...")
        init_db()
        print("✓ Database tables created successfully")
        
        # Create admin user
        print("\n2. Creating default admin user...")
        db = SessionLocal()
        try:
            create_admin_user(db)
        finally:
            db.close()
        
        print("\n" + "=" * 50)
        print("Database initialization completed successfully!")
        print("=" * 50)
        print("\nYou can now start the API server with:")
        print("  uvicorn app.main:app --reload")
        
    except Exception as e:
        print(f"\n❌ Error during initialization: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
