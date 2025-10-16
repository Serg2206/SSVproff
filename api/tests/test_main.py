
"""
Tests for main application endpoints.
"""
import pytest
from fastapi import status


def test_health_endpoint(client):
    """
    Test the health check endpoint returns 200 OK.
    
    Args:
        client: FastAPI test client fixture
    """
    response = client.get("/health")
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "status" in data
    assert data["status"] == "ok"


def test_root_endpoint(client):
    """
    Test the root endpoint returns project information.
    
    Args:
        client: FastAPI test client fixture
    """
    response = client.get("/")
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "name" in data
    assert "version" in data
    assert data["name"] == "SSVproff API"


def test_nonexistent_endpoint(client):
    """
    Test that nonexistent endpoints return 404 Not Found.
    
    Args:
        client: FastAPI test client fixture
    """
    response = client.get("/nonexistent-endpoint")
    
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_health_endpoint_response_structure(client):
    """
    Test that health endpoint returns expected JSON structure.
    
    Args:
        client: FastAPI test client fixture
    """
    response = client.get("/health")
    data = response.json()
    
    # Verify response has required fields
    assert isinstance(data, dict)
    assert "status" in data
    
    # Verify field types
    assert isinstance(data["status"], str)


@pytest.mark.parametrize("endpoint", ["/", "/health"])
def test_cors_headers(client, endpoint):
    """
    Test that CORS headers are present in responses when Origin header is sent.
    
    Args:
        client: FastAPI test client fixture
        endpoint: The endpoint to test
    """
    # Send request with Origin header to trigger CORS
    response = client.get(
        endpoint,
        headers={"Origin": "http://localhost:3000"}
    )
    
    # Check for CORS headers
    assert "access-control-allow-origin" in response.headers
    # Note: Headers are case-insensitive in HTTP


def test_api_accepts_json(client):
    """
    Test that API accepts and processes JSON requests.
    
    Args:
        client: FastAPI test client fixture
    """
    # When POST endpoints are added, test JSON content-type handling
    # For now, verify GET endpoints work
    response = client.get("/", headers={"Content-Type": "application/json"})
    assert response.status_code == status.HTTP_200_OK


def test_api_returns_json(client):
    """
    Test that API returns JSON content type.
    
    Args:
        client: FastAPI test client fixture
    """
    response = client.get("/")
    assert response.headers["content-type"].startswith("application/json")
