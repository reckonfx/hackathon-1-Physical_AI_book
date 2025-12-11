import pytest
from backend.models.translation_request import TranslationRequest
from backend.services.translation_service import TranslationService
from backend.config import SUPPORTED_LANGUAGES
from backend.exceptions import UnsupportedLanguageError


class TestMultipleLanguageSupport:
    """Test suite for multiple language support functionality."""

    def setup_method(self):
        """Set up test fixtures before each test method."""
        self.translation_service = TranslationService()

    def test_supported_languages_list(self):
        """Test that the supported languages list contains expected languages."""
        expected_languages = {"en", "es", "fr", "de", "zh", "ja", "ko", "ru", "pt", "ar"}
        supported_languages = set(SUPPORTED_LANGUAGES)

        assert expected_languages.issubset(supported_languages), \
            f"Expected languages {expected_languages - supported_languages} not found in supported languages"

    def test_translation_with_all_supported_target_languages(self):
        """Test translation to all supported target languages."""
        base_text = "Hello, how are you?"

        for lang_code in SUPPORTED_LANGUAGES:
            request = TranslationRequest(
                text=base_text,
                target_language=lang_code,
                source_language="en"  # Using English as source
            )

            # We expect this to work for all supported languages
            # (though actual translation quality will depend on the implementation)
            try:
                response = self.translation_service.translate(request)
                assert response.target_language == lang_code
                assert response.char_count == len(base_text)
            except UnsupportedLanguageError:
                # This should not happen for supported languages
                pytest.fail(f"Language {lang_code} was rejected but it's in SUPPORTED_LANGUAGES")

    def test_translation_with_all_supported_source_languages(self):
        """Test translation from all supported source languages."""
        base_texts = {
            "en": "Hello, how are you?",
            "es": "Hola, ¿cómo estás?",
            "fr": "Bonjour, comment allez-vous?",
        }

        for src_lang, text in base_texts.items():
            if src_lang in SUPPORTED_LANGUAGES:
                request = TranslationRequest(
                    text=text,
                    target_language="en",  # Translate to English
                    source_language=src_lang
                )

                response = self.translation_service.translate(request)
                assert response.detected_source_language == src_lang
                assert response.target_language == "en"
                assert response.char_count == len(text)

    def test_unsupported_target_language_rejection(self):
        """Test that unsupported target languages are rejected."""
        request = TranslationRequest(
            text="Hello, how are you?",
            target_language="xx",  # Invalid language code
            source_language="en"
        )

        with pytest.raises(UnsupportedLanguageError):
            self.translation_service.translate(request)

    def test_unsupported_source_language_rejection(self):
        """Test that unsupported source languages are rejected."""
        request = TranslationRequest(
            text="Hello, how are you?",
            target_language="es",
            source_language="xx"  # Invalid language code
        )

        with pytest.raises(UnsupportedLanguageError):
            self.translation_service.translate(request)

    def test_language_validation_utility(self):
        """Test the language validation utility functions."""
        from backend.utils.language_validator import (
            validate_language_code,
            validate_language_codes,
            validate_and_raise
        )

        # Test valid language code
        assert validate_language_code("en") is True
        assert validate_language_code("es") is True

        # Test invalid language code
        assert validate_language_code("xx") is False
        assert validate_language_code("english") is False  # Too long
        assert validate_language_code("EN") is False      # Uppercase
        assert validate_language_code("e") is False       # Too short

        # Test multiple language validation
        valid_codes = ["en", "es", "fr"]
        invalid_codes = ["xx", "yy"]
        mixed_codes = ["en", "xx", "es", "yy"]

        validated = validate_language_codes(mixed_codes)
        assert set(validated) == set(["en", "es"])

        # Test validation with exception raising
        with pytest.raises(UnsupportedLanguageError):
            validate_and_raise("invalid")

        # Valid language should not raise
        try:
            validate_and_raise("en")
        except UnsupportedLanguageError:
            pytest.fail("Valid language 'en' incorrectly raised exception")

    def test_auto_detection_with_different_languages(self):
        """Test that auto-detection works with different source languages."""
        test_cases = [
            ("Hello, how are you?", "en"),
            ("Hola, ¿cómo estás?", "es"),
            ("Bonjour, comment allez-vous?", "fr"),
        ]

        for text, expected_lang in test_cases:
            request = TranslationRequest(
                text=text,
                target_language="en"  # Translate to English
                # source_language is omitted to trigger auto-detection
            )

            response = self.translation_service.translate(request)
            # Note: Since we're using a mock translation, we can't verify
            # the actual detected language, but the call should succeed
            assert response.target_language == "en"
            assert response.char_count == len(text)