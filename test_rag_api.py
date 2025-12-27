import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Now import the main app
from backend.main import app

print("RAG API application loaded successfully!")

# Test the API endpoints using TestClient
from fastapi.testclient import TestClient

client = TestClient(app)

def test_api_endpoints():
    print("\nTesting API endpoints:")

    # Test health endpoint
    response = client.get("/api/health")
    print(f"Health endpoint: {response.status_code} - {response.json()}")

    # Test root endpoint
    response = client.get("/")
    print(f"Root endpoint: {response.status_code} - {response.json()}")

    # Test search endpoint (should fail since no content yet, but should not return 404)
    response = client.post("/api/search", json={"query": "ROS2"})
    print(f"Search endpoint status: {response.status_code}")

    # Test validate-content endpoint
    response = client.post("/api/validate-content", json={"content": "This is a test content for RAG."})
    print(f"Validate content endpoint: {response.status_code} - {response.json()}")

    # Test chat endpoint
    response = client.post("/api/chat", json={
        "messages": [
            {"role": "user", "content": "What is ROS2?"}
        ]
    })
    print(f"Chat endpoint status: {response.status_code}")

if __name__ == "__main__":
    test_api_endpoints()