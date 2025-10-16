
"""
Tests for authentication endpoints.
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.db.base import Base
from app.api.deps import get_db
from app.core.security import create_access_token


# Create in-memory SQLite database for testing
TEST_DATABASE_URL = "sqlite:///:memory:"


@pytest.fixture
def test_db():
    """Create a test database."""
    engine = create_engine(
        TEST_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    yield TestingSessionLocal()
    
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client(test_db):
    """Create a test client with test database."""
    def override_get_db():
        try:
            yield test_db
        finally:
            test_db.close()
    
    app.dependency_overrides[get_db] = override_get_db
    
    with TestClient(app) as test_client:
        yield test_client
    
    app.dependency_overrides.clear()


class TestRegistrationEndpoint:
    """Test user registration endpoint."""
    
    def test_register_user_success(self, client):
        """Test successful user registration."""
        response = client.post(
            "/api/v1/auth/register",
            json={
                "email": "test@example.com",
                "username": "testuser",
                "password": "securepassword123"
            }
        )
        
        assert response.status_code == 201
        data = response.json()
        assert data["email"] == "test@example.com"
        assert data["username"] == "testuser"
        assert "hashed_password" not in data
        assert "password" not in data
        assert data["is_active"] is True
        assert data["is_superuser"] is False
        assert "id" in data
        assert "created_at" in data
        assert "updated_at" in data
    
    def test_register_duplicate_email(self, client):
        """Test registration with duplicate email fails."""
        # Register first user
        client.post(
            "/api/v1/auth/register",
            json={
                "email": "test@example.com",
                "username": "user1",
                "password": "password123"
            }
        )
        
        # Try to register with same email
        response = client.post(
            "/api/v1/auth/register",
            json={
                "email": "test@example.com",
                "username": "user2",
                "password": "password123"
            }
        )
        
        assert response.status_code == 400
        assert "email" in response.json()["detail"].lower()
    
    def test_register_duplicate_username(self, client):
        """Test registration with duplicate username fails."""
        # Register first user
        client.post(
            "/api/v1/auth/register",
            json={
                "email": "user1@example.com",
                "username": "testuser",
                "password": "password123"
            }
        )
        
        # Try to register with same username
        response = client.post(
            "/api/v1/auth/register",
            json={
                "email": "user2@example.com",
                "username": "testuser",
                "password": "password123"
            }
        )
        
        assert response.status_code == 400
        assert "username" in response.json()["detail"].lower()
    
    def test_register_invalid_email(self, client):
        """Test registration with invalid email fails."""
        response = client.post(
            "/api/v1/auth/register",
            json={
                "email": "invalid-email",
                "username": "testuser",
                "password": "password123"
            }
        )
        
        assert response.status_code == 422
    
    def test_register_short_password(self, client):
        """Test registration with short password fails."""
        response = client.post(
            "/api/v1/auth/register",
            json={
                "email": "test@example.com",
                "username": "testuser",
                "password": "short"
            }
        )
        
        assert response.status_code == 422
    
    def test_register_invalid_username(self, client):
        """Test registration with invalid username fails."""
        response = client.post(
            "/api/v1/auth/register",
            json={
                "email": "test@example.com",
                "username": "us",  # Too short
                "password": "password123"
            }
        )
        
        assert response.status_code == 422


class TestLoginEndpoint:
    """Test user login endpoint."""
    
    @pytest.fixture
    def registered_user(self, client):
        """Register a user for login tests."""
        response = client.post(
            "/api/v1/auth/register",
            json={
                "email": "test@example.com",
                "username": "testuser",
                "password": "securepassword123"
            }
        )
        return response.json()
    
    def test_login_success(self, client, registered_user):
        """Test successful login."""
        response = client.post(
            "/api/v1/auth/login",
            json={
                "email": "test@example.com",
                "password": "securepassword123"
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data
        assert data["token_type"] == "bearer"
    
    def test_login_wrong_password(self, client, registered_user):
        """Test login with wrong password fails."""
        response = client.post(
            "/api/v1/auth/login",
            json={
                "email": "test@example.com",
                "password": "wrongpassword"
            }
        )
        
        assert response.status_code == 401
    
    def test_login_nonexistent_user(self, client):
        """Test login with nonexistent user fails."""
        response = client.post(
            "/api/v1/auth/login",
            json={
                "email": "nonexistent@example.com",
                "password": "password123"
            }
        )
        
        assert response.status_code == 401


class TestMeEndpoint:
    """Test current user endpoint."""
    
    @pytest.fixture
    def auth_headers(self, client):
        """Register a user and get auth token."""
        # Register user
        client.post(
            "/api/v1/auth/register",
            json={
                "email": "test@example.com",
                "username": "testuser",
                "password": "securepassword123"
            }
        )
        
        # Login
        response = client.post(
            "/api/v1/auth/login",
            json={
                "email": "test@example.com",
                "password": "securepassword123"
            }
        )
        
        token = response.json()["access_token"]
        return {"Authorization": f"Bearer {token}"}
    
    def test_get_current_user_success(self, client, auth_headers):
        """Test getting current user with valid token."""
        response = client.get("/api/v1/auth/me", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == "test@example.com"
        assert data["username"] == "testuser"
        assert "hashed_password" not in data
    
    def test_get_current_user_no_token(self, client):
        """Test getting current user without token fails."""
        response = client.get("/api/v1/auth/me")
        
        assert response.status_code == 401
    
    def test_get_current_user_invalid_token(self, client):
        """Test getting current user with invalid token fails."""
        response = client.get(
            "/api/v1/auth/me",
            headers={"Authorization": "Bearer invalid_token"}
        )
        
        assert response.status_code == 401


class TestRefreshEndpoint:
    """Test token refresh endpoint."""
    
    @pytest.fixture
    def tokens(self, client):
        """Register a user and get tokens."""
        # Register user
        client.post(
            "/api/v1/auth/register",
            json={
                "email": "test@example.com",
                "username": "testuser",
                "password": "securepassword123"
            }
        )
        
        # Login
        response = client.post(
            "/api/v1/auth/login",
            json={
                "email": "test@example.com",
                "password": "securepassword123"
            }
        )
        
        return response.json()
    
    def test_refresh_token_success(self, client, tokens):
        """Test refreshing access token with valid refresh token."""
        response = client.post(
            "/api/v1/auth/refresh",
            json={"refresh_token": tokens["refresh_token"]}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
    
    def test_refresh_token_invalid(self, client):
        """Test refreshing with invalid token fails."""
        response = client.post(
            "/api/v1/auth/refresh",
            json={"refresh_token": "invalid_token"}
        )
        
        assert response.status_code == 401
    
    def test_refresh_token_with_access_token(self, client, tokens):
        """Test that access token cannot be used to refresh."""
        response = client.post(
            "/api/v1/auth/refresh",
            json={"refresh_token": tokens["access_token"]}
        )
        
        assert response.status_code == 401
