
"""
Tests for database operations and user model.
"""
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.db.base import Base
from app.models.user import User
from app.core.security import get_password_hash


# Create in-memory SQLite database for testing
TEST_DATABASE_URL = "sqlite:///:memory:"

@pytest.fixture
def test_db():
    """Create a test database session."""
    engine = create_engine(
        TEST_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
    
    # Create session
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = TestingSessionLocal()
    
    yield db
    
    db.close()
    Base.metadata.drop_all(bind=engine)


class TestUserModel:
    """Test User model operations."""
    
    def test_create_user(self, test_db):
        """Test creating a user."""
        user = User(
            email="test@example.com",
            username="testuser",
            hashed_password=get_password_hash("password123"),
            is_active=True,
            is_superuser=False
        )
        
        test_db.add(user)
        test_db.commit()
        test_db.refresh(user)
        
        assert user.id is not None
        assert user.email == "test@example.com"
        assert user.username == "testuser"
        assert user.is_active is True
        assert user.is_superuser is False
        assert user.created_at is not None
        assert user.updated_at is not None
    
    def test_user_unique_email(self, test_db):
        """Test email uniqueness constraint."""
        user1 = User(
            email="test@example.com",
            username="user1",
            hashed_password=get_password_hash("password123")
        )
        user2 = User(
            email="test@example.com",
            username="user2",
            hashed_password=get_password_hash("password123")
        )
        
        test_db.add(user1)
        test_db.commit()
        
        test_db.add(user2)
        with pytest.raises(Exception):  # SQLAlchemy will raise IntegrityError
            test_db.commit()
    
    def test_user_unique_username(self, test_db):
        """Test username uniqueness constraint."""
        user1 = User(
            email="user1@example.com",
            username="testuser",
            hashed_password=get_password_hash("password123")
        )
        user2 = User(
            email="user2@example.com",
            username="testuser",
            hashed_password=get_password_hash("password123")
        )
        
        test_db.add(user1)
        test_db.commit()
        
        test_db.add(user2)
        with pytest.raises(Exception):  # SQLAlchemy will raise IntegrityError
            test_db.commit()
    
    def test_query_user_by_email(self, test_db):
        """Test querying user by email."""
        user = User(
            email="test@example.com",
            username="testuser",
            hashed_password=get_password_hash("password123")
        )
        
        test_db.add(user)
        test_db.commit()
        
        found_user = test_db.query(User).filter(User.email == "test@example.com").first()
        
        assert found_user is not None
        assert found_user.email == "test@example.com"
        assert found_user.username == "testuser"
    
    def test_user_repr(self, test_db):
        """Test user string representation."""
        user = User(
            email="test@example.com",
            username="testuser",
            hashed_password=get_password_hash("password123")
        )
        
        test_db.add(user)
        test_db.commit()
        test_db.refresh(user)
        
        repr_str = repr(user)
        assert "User" in repr_str
        assert "test@example.com" in repr_str
        assert "testuser" in repr_str
