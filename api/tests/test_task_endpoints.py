
"""
Tests for task endpoints (example of protected CRUD operations).
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.db.base import Base
from app.api.deps import get_db


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


@pytest.fixture
def auth_headers(client):
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


@pytest.fixture
def second_user_headers(client):
    """Register a second user and get auth token."""
    # Register user
    client.post(
        "/api/v1/auth/register",
        json={
            "email": "second@example.com",
            "username": "seconduser",
            "password": "securepassword123"
        }
    )
    
    # Login
    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "second@example.com",
            "password": "securepassword123"
        }
    )
    
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


class TestCreateTask:
    """Test task creation endpoint."""
    
    def test_create_task_success(self, client, auth_headers):
        """Test successful task creation."""
        response = client.post(
            "/api/v1/tasks/",
            headers=auth_headers,
            json={
                "title": "Complete project",
                "description": "Finish the API implementation",
                "is_completed": False
            }
        )
        
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "Complete project"
        assert data["description"] == "Finish the API implementation"
        assert data["is_completed"] is False
        assert "id" in data
        assert "owner_id" in data
        assert "created_at" in data
        assert "updated_at" in data
    
    def test_create_task_without_auth(self, client):
        """Test that creating task without auth fails."""
        response = client.post(
            "/api/v1/tasks/",
            json={
                "title": "Complete project",
                "description": "Finish the API implementation"
            }
        )
        
        assert response.status_code == 401
    
    def test_create_task_minimal(self, client, auth_headers):
        """Test creating task with minimal fields."""
        response = client.post(
            "/api/v1/tasks/",
            headers=auth_headers,
            json={
                "title": "Simple task"
            }
        )
        
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "Simple task"
        assert data["description"] is None
        assert data["is_completed"] is False
    
    def test_create_task_invalid_data(self, client, auth_headers):
        """Test creating task with invalid data fails."""
        response = client.post(
            "/api/v1/tasks/",
            headers=auth_headers,
            json={
                "title": ""  # Empty title
            }
        )
        
        assert response.status_code == 422


class TestListTasks:
    """Test task listing endpoint."""
    
    @pytest.fixture
    def sample_tasks(self, client, auth_headers):
        """Create sample tasks for testing."""
        tasks = []
        for i in range(5):
            response = client.post(
                "/api/v1/tasks/",
                headers=auth_headers,
                json={
                    "title": f"Task {i}",
                    "description": f"Description {i}",
                    "is_completed": i % 2 == 0
                }
            )
            tasks.append(response.json())
        return tasks
    
    def test_list_tasks_success(self, client, auth_headers, sample_tasks):
        """Test listing all user tasks."""
        response = client.get("/api/v1/tasks/", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 5
        assert all("id" in task for task in data)
    
    def test_list_tasks_without_auth(self, client):
        """Test that listing tasks without auth fails."""
        response = client.get("/api/v1/tasks/")
        
        assert response.status_code == 401
    
    def test_list_tasks_filter_completed(self, client, auth_headers, sample_tasks):
        """Test filtering tasks by completion status."""
        response = client.get(
            "/api/v1/tasks/?completed=true",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 3  # Tasks 0, 2, 4 are completed
        assert all(task["is_completed"] for task in data)
    
    def test_list_tasks_filter_incomplete(self, client, auth_headers, sample_tasks):
        """Test filtering incomplete tasks."""
        response = client.get(
            "/api/v1/tasks/?completed=false",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2  # Tasks 1, 3 are incomplete
        assert all(not task["is_completed"] for task in data)
    
    def test_list_tasks_pagination(self, client, auth_headers, sample_tasks):
        """Test task pagination."""
        response = client.get(
            "/api/v1/tasks/?skip=2&limit=2",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
    
    def test_list_tasks_empty(self, client, auth_headers):
        """Test listing tasks when user has no tasks."""
        response = client.get("/api/v1/tasks/", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 0
    
    def test_list_tasks_user_isolation(self, client, auth_headers, second_user_headers, sample_tasks):
        """Test that users can only see their own tasks."""
        # First user has 5 tasks from sample_tasks fixture
        # Second user should see no tasks
        response = client.get("/api/v1/tasks/", headers=second_user_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 0


class TestGetTask:
    """Test getting a specific task endpoint."""
    
    @pytest.fixture
    def sample_task(self, client, auth_headers):
        """Create a sample task."""
        response = client.post(
            "/api/v1/tasks/",
            headers=auth_headers,
            json={
                "title": "Sample task",
                "description": "Sample description"
            }
        )
        return response.json()
    
    def test_get_task_success(self, client, auth_headers, sample_task):
        """Test getting a specific task."""
        task_id = sample_task["id"]
        response = client.get(f"/api/v1/tasks/{task_id}", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == task_id
        assert data["title"] == "Sample task"
    
    def test_get_task_not_found(self, client, auth_headers):
        """Test getting a non-existent task."""
        fake_id = "123e4567-e89b-12d3-a456-426614174000"
        response = client.get(f"/api/v1/tasks/{fake_id}", headers=auth_headers)
        
        assert response.status_code == 404
    
    def test_get_task_without_auth(self, client, sample_task):
        """Test getting task without authentication."""
        task_id = sample_task["id"]
        response = client.get(f"/api/v1/tasks/{task_id}")
        
        assert response.status_code == 401
    
    def test_get_task_wrong_owner(self, client, auth_headers, second_user_headers, sample_task):
        """Test that user cannot get another user's task."""
        task_id = sample_task["id"]
        # Try to get first user's task with second user's token
        response = client.get(f"/api/v1/tasks/{task_id}", headers=second_user_headers)
        
        assert response.status_code == 404


class TestUpdateTask:
    """Test task update endpoint."""
    
    @pytest.fixture
    def sample_task(self, client, auth_headers):
        """Create a sample task."""
        response = client.post(
            "/api/v1/tasks/",
            headers=auth_headers,
            json={
                "title": "Original title",
                "description": "Original description",
                "is_completed": False
            }
        )
        return response.json()
    
    def test_update_task_success(self, client, auth_headers, sample_task):
        """Test successful task update."""
        task_id = sample_task["id"]
        response = client.put(
            f"/api/v1/tasks/{task_id}",
            headers=auth_headers,
            json={
                "title": "Updated title",
                "is_completed": True
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Updated title"
        assert data["is_completed"] is True
        # Description should remain unchanged
        assert data["description"] == "Original description"
    
    def test_update_task_partial(self, client, auth_headers, sample_task):
        """Test partial task update."""
        task_id = sample_task["id"]
        response = client.put(
            f"/api/v1/tasks/{task_id}",
            headers=auth_headers,
            json={"is_completed": True}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["is_completed"] is True
        assert data["title"] == "Original title"
    
    def test_update_task_not_found(self, client, auth_headers):
        """Test updating a non-existent task."""
        fake_id = "123e4567-e89b-12d3-a456-426614174000"
        response = client.put(
            f"/api/v1/tasks/{fake_id}",
            headers=auth_headers,
            json={"title": "Updated"}
        )
        
        assert response.status_code == 404
    
    def test_update_task_without_auth(self, client, sample_task):
        """Test updating task without authentication."""
        task_id = sample_task["id"]
        response = client.put(
            f"/api/v1/tasks/{task_id}",
            json={"title": "Updated"}
        )
        
        assert response.status_code == 401
    
    def test_update_task_wrong_owner(self, client, auth_headers, second_user_headers, sample_task):
        """Test that user cannot update another user's task."""
        task_id = sample_task["id"]
        # Try to update first user's task with second user's token
        response = client.put(
            f"/api/v1/tasks/{task_id}",
            headers=second_user_headers,
            json={"title": "Hacked"}
        )
        
        assert response.status_code == 404


class TestDeleteTask:
    """Test task deletion endpoint."""
    
    @pytest.fixture
    def sample_task(self, client, auth_headers):
        """Create a sample task."""
        response = client.post(
            "/api/v1/tasks/",
            headers=auth_headers,
            json={
                "title": "Task to delete",
                "description": "This will be deleted"
            }
        )
        return response.json()
    
    def test_delete_task_success(self, client, auth_headers, sample_task):
        """Test successful task deletion."""
        task_id = sample_task["id"]
        response = client.delete(f"/api/v1/tasks/{task_id}", headers=auth_headers)
        
        assert response.status_code == 204
        
        # Verify task is deleted
        get_response = client.get(f"/api/v1/tasks/{task_id}", headers=auth_headers)
        assert get_response.status_code == 404
    
    def test_delete_task_not_found(self, client, auth_headers):
        """Test deleting a non-existent task."""
        fake_id = "123e4567-e89b-12d3-a456-426614174000"
        response = client.delete(f"/api/v1/tasks/{fake_id}", headers=auth_headers)
        
        assert response.status_code == 404
    
    def test_delete_task_without_auth(self, client, sample_task):
        """Test deleting task without authentication."""
        task_id = sample_task["id"]
        response = client.delete(f"/api/v1/tasks/{task_id}")
        
        assert response.status_code == 401
    
    def test_delete_task_wrong_owner(self, client, auth_headers, second_user_headers, sample_task):
        """Test that user cannot delete another user's task."""
        task_id = sample_task["id"]
        # Try to delete first user's task with second user's token
        response = client.delete(f"/api/v1/tasks/{task_id}", headers=second_user_headers)
        
        assert response.status_code == 404
        
        # Verify task still exists for original owner
        get_response = client.get(f"/api/v1/tasks/{task_id}", headers=auth_headers)
        assert get_response.status_code == 200
