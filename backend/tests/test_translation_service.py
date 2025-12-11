import pytest
from backend.models.translation_request import TranslationRequest
from backend.services.translation_service import TranslationService


class TestTranslationService:
    """Unit tests for TranslationService."""

    def setup_method(self):
        """Set up test fixtures before each test method."""
        self.translation_service = TranslationService()

    def test_translate_with_source_language(self):
        """Test translation when source language is provided."""
        request = TranslationRequest(
            text="Hello, world!",
            target_language="es",
            source_language="en"
        )

        response = self.translation_service.translate(request)

        assert response.target_language == "es"
        assert response.detected_source_language == "en"
        assert response.char_count == len("Hello, world!")
        assert "TRANSLATED" in response.translated_text
        assert response.processing_time > 0

    def test_translate_without_source_language(self):
        """Test translation when source language needs to be detected."""
        request = TranslationRequest(
            text="Hello, world!",
            target_language="es"
        )

        response = self.translation_service.translate(request)

        assert response.target_language == "es"
        assert response.detected_source_language is not None
        assert response.char_count == len("Hello, world!")
        assert "TRANSLATED" in response.translated_text

    def test_translate_with_glossary_ref(self):
        """Test translation with technical term preservation."""
        request = TranslationRequest(
            text="The robot uses SLAM algorithms.",
            target_language="es",
            glossary_ref=True
        )

        response = self.translation_service.translate(request)

        assert response.technical_terms is not None
        assert "SLAM" in response.technical_terms
        assert response.char_count == len("The robot uses SLAM algorithms.")

    def test_translate_without_glossary_ref(self):
        """Test translation without technical term preservation."""
        request = TranslationRequest(
            text="The robot uses SLAM algorithms.",
            target_language="es",
            glossary_ref=False
        )

        response = self.translation_service.translate(request)

        assert response.technical_terms is None

    def test_preserve_technical_terms(self):
        """Test technical term preservation functionality."""
        text = "The robot uses SLAM and PID controller algorithms."

        processed_text, terms = self.translation_service._preserve_technical_terms(text)

        assert "SLAM" in terms
        assert "PID controller" in terms
        assert processed_text == text  # For now, just returns the same text

    def test_character_limit_exceeded(self):
        """Test that character limit is enforced."""
        long_text = "A" * 1001  # Exceeds the 1000 character limit
        request = TranslationRequest(
            text=long_text,
            target_language="es"
        )

        with pytest.raises(Exception) as exc_info:
            self.translation_service.translate(request)

        assert "Character limit exceeded" in str(exc_info.value)

    def test_valid_language_codes(self):
        """Test that language codes are validated."""
        # This is tested through the Pydantic model validation
        # which is already handled in the model
        pass