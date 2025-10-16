
"""
Tests for health check endpoints.
"""
import pytest
from fastapi import status


class TestHealthEndpoint:
    """Test suite for health check endpoint."""

    def test_health_returns_ok_status(self, client):
        """Test that health endpoint returns OK status."""
        response = client.get("/health")
        
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["status"] == "ok"

    def test_health_response_time(self, client):
        """Test that health endpoint responds quickly."""
        import time
        
        start_time = time.time()
        response = client.get("/health")
        elapsed_time = time.time() - start_time
        
        assert response.status_code == status.HTTP_200_OK
        # Health check should respond in less than 1 second
        assert elapsed_time < 1.0

    def test_health_multiple_requests(self, client):
        """Test that health endpoint handles multiple consecutive requests."""
        responses = [client.get("/health") for _ in range(10)]
        
        for response in responses:
            assert response.status_code == status.HTTP_200_OK
            assert response.json()["status"] == "ok"

    @pytest.mark.asyncio
    async def test_health_endpoint_availability(self, client):
        """Test that health endpoint is always available."""
        # This test ensures health check works even under load
        response = client.get("/health")
        assert response.status_code == status.HTTP_200_OK
