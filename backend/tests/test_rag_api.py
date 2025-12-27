import pytest
from fastapi.testclient import TestClient

# Import your main app
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from main import app

client = TestClient(app)

def test_health_endpoint():
    """Test the health endpoint"""
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["version"] == "1.0.0"

def test_root_endpoint():
    """Test the root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "Physical AI Book RAG API" in data["message"]

def test_search_endpoint_exists():
    """Test that search endpoint is available"""
    # This will fail initially since we're searching for content that may not exist
    # but it should return a 422 (validation error) or 500, not 404 (not found)
    response = client.post("/api/search", json={"query": "test"})
    assert response.status_code != 404  # Should exist even if search fails

if __name__ == "__main__":
    pytest.main([__file__])