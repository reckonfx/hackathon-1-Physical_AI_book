import time
import re
from typing import List, Optional
from backend.models.translation_request import TranslationRequest
from backend.models.translation_response import TranslationResponse
from backend.models.language_detection_request import LanguageDetectionRequest
from backend.models.language_detection_response import LanguageDetectionResponse
from backend.services.language_detection_service import LanguageDetectionService
from backend.config import CHARACTER_LIMIT, TECHNICAL_TERMS_LIST, SUPPORTED_LANGUAGES
from backend.exceptions import CharacterLimitExceededError, TranslationError, UnsupportedLanguageError


class TranslationService:
    """
    Core translation service that handles text translation between languages.
    """

    def __init__(self):
        self.language_detection_service = LanguageDetectionService()

    def translate(self, request: TranslationRequest) -> TranslationResponse:
        """
        Translate text from source language to target language.

        Args:
            request: TranslationRequest containing text and target language

        Returns:
            TranslationResponse with translated text and metadata
        """
        start_time = time.time()

        # Check character limit
        if len(request.text) > CHARACTER_LIMIT:
            raise CharacterLimitExceededError(len(request.text), CHARACTER_LIMIT)

        # Validate target language
        if request.target_language not in SUPPORTED_LANGUAGES:
            raise UnsupportedLanguageError(request.target_language)

        # Validate source language if provided
        if request.source_language and request.source_language not in SUPPORTED_LANGUAGES:
            raise UnsupportedLanguageError(request.source_language)

        # Detect source language if not provided
        detected_source_language = None
        if not request.source_language:
            detection_request = LanguageDetectionRequest(text=request.text)
            detection_response = self.language_detection_service.detect_language(detection_request)
            detected_source_language = detection_response.detected_language
            # Use confidence from detection if available
            detection_confidence = detection_response.confidence
        else:
            detected_source_language = request.source_language
            detection_confidence = 1.0  # 100% confidence since it was provided

        # Process technical terms if requested
        technical_terms = []
        processed_text = request.text
        if request.glossary_ref:
            processed_text, technical_terms = self._preserve_technical_terms(request.text)

        # Perform the translation (simulated for now)
        translated_text = self._perform_translation(
            processed_text,
            detected_source_language,
            request.target_language
        )

        # Calculate processing time
        processing_time = (time.time() - start_time) * 1000  # Convert to milliseconds

        # Create response
        response = TranslationResponse(
            translated_text=translated_text,
            detected_source_language=detected_source_language,
            target_language=request.target_language,
            confidence=0.95,  # Simulated confidence
            technical_terms=technical_terms if request.glossary_ref else None,
            char_count=len(request.text),
            processing_time=processing_time
        )

        return response

    def _preserve_technical_terms(self, text: str) -> tuple[str, List[str]]:
        """
        Identify and preserve technical terms in the text.

        Args:
            text: Input text to process

        Returns:
            Tuple of (processed text, list of technical terms found)
        """
        found_terms = []
        processed_text = text

        for term in TECHNICAL_TERMS_LIST:
            # Use word boundaries to match exact terms
            pattern = r'\b' + re.escape(term) + r'\b'
            matches = re.findall(pattern, text, re.IGNORECASE)
            found_terms.extend([match for match in matches if match.lower() == term.lower()])

        # Remove duplicates while preserving order
        seen = set()
        unique_terms = []
        for term in found_terms:
            term_lower = term.lower()
            if term_lower not in seen:
                seen.add(term_lower)
                unique_terms.append(term)

        return processed_text, unique_terms

    def _perform_translation(self, text: str, source_lang: str, target_lang: str) -> str:
        """
        Perform the actual translation (placeholder implementation).

        In a real implementation, this would call an external translation API.
        For now, it returns a simple transformation for demonstration purposes.
        """
        # This is a placeholder - in real implementation, call translation API
        # For demonstration, we'll just return the original text with a prefix
        # to simulate translation
        return f"[TRANSLATED] {text} [FROM: {source_lang} TO: {target_lang}]"