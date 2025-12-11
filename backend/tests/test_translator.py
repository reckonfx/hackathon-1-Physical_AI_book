import pytest
from fastapi.testclient import TestClient
from backend.api.v1.translator import router
from backend.models.translation_request import TranslationRequest
from fastapi import FastAPI


# Create a test app with the router
app = FastAPI()
app.include_router(router)

client = TestClient(app)


class TestTranslatorAPI:
    """Integration tests for the translator API endpoints."""

    def test_translate_endpoint_success(self):
        """Test successful translation request."""
        payload = {
            "text": "Hello, world!",
            "target_language": "es",
            "source_language": "en"
        }

        response = client.post("/translate/", json=payload)

        assert response.status_code == 200
        data = response.json()
        assert "translated_text" in data
        assert data["target_language"] == "es"
        assert data["detected_source_language"] == "en"
        assert "char_count" in data
        assert "processing_time" in data
        assert "TRANSLATED" in data["translated_text"]

    def test_translate_endpoint_without_source_language(self):
        """Test translation request without source language (auto-detect)."""
        payload = {
            "text": "Hello, world!",
            "target_language": "es"
        }

        response = client.post("/translate/", json=payload)

        assert response.status_code == 200
        data = response.json()
        assert "translated_text" in data
        assert data["target_language"] == "es"
        assert "char_count" in data
        assert "processing_time" in data

    def test_translate_endpoint_with_glossary_ref(self):
        """Test translation with glossary reference."""
        payload = {
            "text": "The robot uses SLAM algorithms.",
            "target_language": "es",
            "glossary_ref": True
        }

        response = client.post("/translate/", json=payload)

        assert response.status_code == 200
        data = response.json()
        assert "translated_text" in data
        assert "technical_terms" in data
        assert data["technical_terms"] is not None

    def test_translate_endpoint_without_glossary_ref(self):
        """Test translation without glossary reference."""
        payload = {
            "text": "The robot uses SLAM algorithms.",
            "target_language": "es",
            "glossary_ref": False
        }

        response = client.post("/translate/", json=payload)

        assert response.status_code == 200
        data = response.json()
        assert "translated_text" in data

    def test_translate_endpoint_missing_required_fields(self):
        """Test translation request with missing required fields."""
        # Missing text
        payload = {
            "target_language": "es"
        }

        response = client.post("/translate/", json=payload)
        assert response.status_code == 422  # Validation error

        # Missing target_language
        payload = {
            "text": "Hello, world!"
        }

        response = client.post("/translate/", json=payload)
        assert response.status_code == 422  # Validation error

    def test_translate_endpoint_invalid_language_code(self):
        """Test translation request with invalid language code."""
        payload = {
            "text": "Hello, world!",
            "target_language": "invalid"  # Invalid language code
        }

        response = client.post("/translate/", json=payload)
        assert response.status_code == 422  # Validation error due to pattern mismatch

    def test_translate_endpoint_text_too_long(self):
        """Test translation request with text exceeding character limit."""
        long_text = "A" * 1001  # Exceeds 1000 character limit
        payload = {
            "text": long_text,
            "target_language": "es"
        }

        response = client.post("/translate/", json=payload)
        assert response.status_code == 500  # Character limit exceeded error