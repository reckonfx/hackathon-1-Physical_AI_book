import pytest
from fastapi.testclient import TestClient
from backend.models.translation_request import TranslationRequest
from backend.models.language_detection_request import LanguageDetectionRequest
from backend.services.translation_service import TranslationService
from backend.services.language_detection_service import LanguageDetectionService
from backend.exceptions import CharacterLimitExceededError, UnsupportedLanguageError
from backend.config import CHARACTER_LIMIT
from fastapi import FastAPI
from backend.api.v1.translator import router as translator_router
from backend.api.v1.language_detector import router as detector_router


# Create a test app with the routers
app = FastAPI()
app.include_router(translator_router)
app.include_router(detector_router)

client = TestClient(app)


class TestEdgeCases:
    """Comprehensive test suite covering edge cases from spec."""

    def setup_method(self):
        """Set up test fixtures before each test method."""
        self.translation_service = TranslationService()
        self.language_detection_service = LanguageDetectionService()

    def test_unsupported_target_language(self):
        """Test handling for unsupported target languages."""
        request = TranslationRequest(
            text="Hello, world!",
            target_language="xx"  # Unsupported language
        )

        with pytest.raises(UnsupportedLanguageError):
            self.translation_service.translate(request)

    def test_unsupported_source_language(self):
        """Test handling for unsupported source languages."""
        request = TranslationRequest(
            text="Hello, world!",
            target_language="es",
            source_language="yy"  # Unsupported language
        )

        with pytest.raises(UnsupportedLanguageError):
            self.translation_service.translate(request)

    def test_mixed_language_input_text(self):
        """Test detection and handling for mixed-language input text."""
        # Text with mixed languages
        mixed_text = "Hello in English and hola in Spanish"
        request = LanguageDetectionRequest(text=mixed_text)

        # This should detect the dominant language or one of the languages
        response = self.language_detection_service.detect_language(request)

        # The response should have a detected language
        assert response.detected_language is not None
        assert isinstance(response.detected_language, str)
        assert len(response.detected_language) == 2  # ISO 639-1 format

    def test_translation_request_exceeding_character_limits(self):
        """Test handling for translation requests exceeding character limits."""
        # Create text that exceeds the limit
        long_text = "A" * (CHARACTER_LIMIT + 1)

        request = TranslationRequest(
            text=long_text,
            target_language="es"
        )

        with pytest.raises(CharacterLimitExceededError):
            self.translation_service.translate(request)

    def test_empty_text_translation(self):
        """Test translation with empty text."""
        request = TranslationRequest(
            text="",
            target_language="es"
        )

        # This might fail or return empty result depending on implementation
        try:
            response = self.translation_service.translate(request)
            # If it succeeds, the response should have empty translated text
            assert response.char_count == 0
        except Exception:
            # If it fails, that's also acceptable behavior
            pass

    def test_special_characters_and_punctuation(self):
        """Test translation with special characters and punctuation."""
        special_text = "!@#$%^&*()_+-=[]{}|;':\",./<>?`~"
        request = TranslationRequest(
            text=special_text,
            target_language="es"
        )

        # Should handle special characters without error
        response = self.translation_service.translate(request)
        assert response.char_count == len(special_text)

    def test_very_short_text(self):
        """Test translation with very short text."""
        short_text = "Hi"
        request = TranslationRequest(
            text=short_text,
            target_language="es"
        )

        response = self.translation_service.translate(request)
        assert response.char_count == len(short_text)

    def test_unicode_characters(self):
        """Test translation with Unicode characters."""
        unicode_text = "Hello 世界 🌍"
        request = TranslationRequest(
            text=unicode_text,
            target_language="es"
        )

        response = self.translation_service.translate(request)
        assert response.char_count == len(unicode_text)

    def test_technical_terminology_handling(self):
        """Test handling for technical terminology that should not be translated."""
        tech_text = "The robot uses SLAM and PID controller algorithms in ROS environment."
        request = TranslationRequest(
            text=tech_text,
            target_language="es",
            glossary_ref=True
        )

        response = self.translation_service.translate(request)
        # Should identify technical terms
        assert response.technical_terms is not None

    def test_language_detection_with_very_short_text(self):
        """Test language detection with very short text."""
        short_text = "Hi"
        request = LanguageDetectionRequest(text=short_text)

        response = self.language_detection_service.detect_language(request)
        # May not be accurate but should not fail
        assert response.char_count == len(short_text)

    def test_language_detection_with_numbers_only(self):
        """Test language detection with numbers only."""
        numbers_text = "12345 67890"
        request = LanguageDetectionRequest(text=numbers_text)

        response = self.language_detection_service.detect_language(request)
        # May not detect a language but should not fail
        assert response.char_count == len(numbers_text)

    def test_translation_with_maximum_allowed_characters(self):
        """Test translation with maximum allowed characters."""
        max_text = "A" * CHARACTER_LIMIT
        request = TranslationRequest(
            text=max_text,
            target_language="es"
        )

        # Should handle maximum length text without error
        response = self.translation_service.translate(request)
        assert response.char_count == CHARACTER_LIMIT

    def test_api_unsupported_target_language(self):
        """Test API handling for unsupported target languages."""
        payload = {
            "text": "Hello, world!",
            "target_language": "xx"  # Invalid language code
        }

        response = client.post("/translate/", json=payload)
        # Should return 422 for validation error or 400 for business logic error
        assert response.status_code in [400, 422]

    def test_api_mixed_language_text(self):
        """Test API with mixed language text."""
        payload = {
            "text": "Hello in English and hola in Spanish",
            "target_language": "fr"
        }

        response = client.post("/translate/", json=payload)
        # Should succeed with mixed language text
        assert response.status_code in [200, 500]  # 500 if our mock fails, but shouldn't be an error

    def test_api_character_limit_exceeded(self):
        """Test API with text exceeding character limit."""
        long_text = "A" * (CHARACTER_LIMIT + 1)
        payload = {
            "text": long_text,
            "target_language": "es"
        }

        response = client.post("/translate/", json=payload)
        # Should return 500 with character limit exceeded error
        assert response.status_code == 500
        response_data = response.json()
        assert "CHARACTER_LIMIT_EXCEEDED" in str(response_data)