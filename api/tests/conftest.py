
"""
Pytest configuration and fixtures for API tests.
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.db.base import Base
from app.api.deps import get_db


# Use in-memory SQLite for testing
TEST_DATABASE_URL = "sqlite:///:memory:"


@pytest.fixture
def test_db_engine():
    """
    Create a test database engine.
    
    Returns:
        Engine: SQLAlchemy engine for testing
    """
    engine = create_engine(
        TEST_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    
    yield engine
    
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def test_db_session(test_db_engine):
    """
    Create a test database session.
    
    Args:
        test_db_engine: Test database engine
        
    Yields:
        Session: SQLAlchemy session for testing
    """
    TestingSessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=test_db_engine
    )
    session = TestingSessionLocal()
    
    yield session
    
    session.close()


@pytest.fixture
def client(test_db_session):
    """
    Create a test client with test database dependency override.
    
    Args:
        test_db_session: Test database session
        
    Yields:
        TestClient: A test client instance for making requests to the API
    
    Example:
        >>> def test_health(client):
        ...     response = client.get("/health")
        ...     assert response.status_code == 200
    """
    def override_get_db():
        try:
            yield test_db_session
        finally:
            pass  # Session cleanup handled by fixture
    
    app.dependency_overrides[get_db] = override_get_db
    
    with TestClient(app) as test_client:
        yield test_client
    
    # Clear overrides after test
    app.dependency_overrides.clear()


@pytest.fixture
def test_user():
    """
    Provide a test user data dictionary.
    
    Returns:
        dict: A dictionary containing test user data
    
    Example:
        >>> def test_create_user(client, test_user):
        ...     response = client.post("/api/v1/auth/register", json=test_user)
        ...     assert response.status_code == 201
    """
    return {
        "email": "test@example.com",
        "username": "testuser",
        "password": "securepassword123",
    }


@pytest.fixture
def auth_headers(client, test_user):
    """
    Provide authentication headers for protected endpoints.
    
    Args:
        client: Test client
        test_user: Test user data
        
    Returns:
        dict: A dictionary containing authorization headers
    
    Example:
        >>> def test_protected_route(client, auth_headers):
        ...     response = client.get("/api/v1/auth/me", headers=auth_headers)
        ...     assert response.status_code == 200
    """
    # Register user
    client.post("/api/v1/auth/register", json=test_user)
    
    # Login to get token
    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": test_user["email"],
            "password": test_user["password"]
        }
    )
    
    token = response.json()["access_token"]
    
    return {
        "Authorization": f"Bearer {token}",
    }
