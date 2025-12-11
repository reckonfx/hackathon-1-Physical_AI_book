import pytest
from backend.models.language_detection_request import LanguageDetectionRequest
from backend.services.language_detection_service import LanguageDetectionService


class TestLanguageDetectionService:
    """Unit tests for LanguageDetectionService."""

    def setup_method(self):
        """Set up test fixtures before each test method."""
        self.language_detection_service = LanguageDetectionService()

    def test_detect_language_english(self):
        """Test language detection for English text."""
        request = LanguageDetectionRequest(text="Hello, how are you today?")

        response = self.language_detection_service.detect_language(request)

        assert response.detected_language == "en"
        assert response.char_count == len("Hello, how are you today?")
        assert response.confidence is not None
        assert 0 <= response.confidence <= 1
        assert response.all_matches is not None
        assert len(response.all_matches) > 0

    def test_detect_language_spanish(self):
        """Test language detection for Spanish text."""
        request = LanguageDetectionRequest(text="Hola, ¿cómo estás hoy?")

        response = self.language_detection_service.detect_language(request)

        assert response.detected_language == "es"
        assert response.char_count == len("Hola, ¿cómo estás hoy?")
        assert response.confidence is not None
        assert 0 <= response.confidence <= 1

    def test_detect_language_french(self):
        """Test language detection for French text."""
        request = LanguageDetectionRequest(text="Bonjour, comment allez-vous?")

        response = self.language_detection_service.detect_language(request)

        assert response.detected_language == "fr"
        assert response.char_count == len("Bonjour, comment allez-vous?")
        assert response.confidence is not None
        assert 0 <= response.confidence <= 1

    def test_detect_language_with_mixed_content(self):
        """Test language detection for mixed content."""
        request = LanguageDetectionRequest(text="This is English and le français")

        response = self.language_detection_service.detect_language(request)

        assert response.char_count == len("This is English and le français")
        assert response.confidence is not None
        assert 0 <= response.confidence <= 1
        assert response.all_matches is not None

    def test_detect_language_short_text(self):
        """Test language detection for short text."""
        request = LanguageDetectionRequest(text="Hello")

        response = self.language_detection_service.detect_language(request)

        assert response.char_count == len("Hello")
        assert response.confidence is not None

    def test_all_matches_structure(self):
        """Test that all_matches contains properly structured data."""
        request = LanguageDetectionRequest(text="Hello world")

        response = self.language_detection_service.detect_language(request)

        assert response.all_matches is not None
        for match in response.all_matches:
            assert hasattr(match, 'language')
            assert hasattr(match, 'confidence')
            assert isinstance(match.language, str)
            assert len(match.language) == 2  # ISO 639-1 format
            assert 0 <= match.confidence <= 1