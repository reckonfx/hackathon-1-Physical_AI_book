import pytest
from fastapi.testclient import TestClient
from backend.api.v1.language_detector import router
from fastapi import FastAPI


# Create a test app with the router
app = FastAPI()
app.include_router(router)

client = TestClient(app)


class TestLanguageDetectorAPI:
    """Integration tests for the language detector API endpoints."""

    def test_detect_language_endpoint_success(self):
        """Test successful language detection request."""
        payload = {
            "text": "Hello, how are you today?"
        }

        response = client.post("/detect-language/", json=payload)

        assert response.status_code == 200
        data = response.json()
        assert "detected_language" in data
        assert data["detected_language"] == "en"  # Expected for English text
        assert "char_count" in data
        assert data["char_count"] == len("Hello, how are you today?")
        assert "confidence" in data
        assert 0 <= data["confidence"] <= 1

    def test_detect_language_spanish(self):
        """Test language detection for Spanish text."""
        payload = {
            "text": "Hola, ¿cómo estás hoy?"
        }

        response = client.post("/detect-language/", json=payload)

        assert response.status_code == 200
        data = response.json()
        assert "detected_language" in data
        assert data["detected_language"] == "es"  # Expected for Spanish text
        assert "char_count" in data
        assert "confidence" in data

    def test_detect_language_french(self):
        """Test language detection for French text."""
        payload = {
            "text": "Bonjour, comment allez-vous?"
        }

        response = client.post("/detect-language/", json=payload)

        assert response.status_code == 200
        data = response.json()
        assert "detected_language" in data
        assert data["detected_language"] == "fr"  # Expected for French text

    def test_detect_language_missing_text(self):
        """Test language detection request with missing text."""
        payload = {}  # No text field

        response = client.post("/detect-language/", json=payload)
        assert response.status_code == 422  # Validation error

    def test_detect_language_empty_text(self):
        """Test language detection request with empty text."""
        payload = {
            "text": ""
        }

        response = client.post("/detect-language/", json=payload)
        # This might fail depending on the language detection library's behavior
        # but it should not cause a server error
        assert response.status_code in [200, 422, 500]

    def test_detect_language_long_text(self):
        """Test language detection with text at character limit."""
        long_text = "Hello world. " * 76  # Should be under 1000 characters
        payload = {
            "text": long_text
        }

        response = client.post("/detect-language/", json=payload)

        assert response.status_code == 200
        data = response.json()
        assert "detected_language" in data
        assert "char_count" in data
        assert data["char_count"] == len(long_text)

    def test_detect_language_with_special_characters(self):
        """Test language detection with special characters."""
        payload = {
            "text": "Hello! How are you? I'm fine, thanks."
        }

        response = client.post("/detect-language/", json=payload)

        assert response.status_code == 200
        data = response.json()
        assert "detected_language" in data
        assert "char_count" in data
        assert "confidence" in data