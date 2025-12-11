from typing import List, Tuple
from langdetect import detect, detect_langs
from backend.models.language_detection_request import LanguageDetectionRequest
from backend.models.language_detection_response import LanguageDetectionResponse, LanguageMatch
from backend.config import SUPPORTED_LANGUAGES
from backend.exceptions import LanguageDetectionError


class LanguageDetectionService:
    """
    Service for detecting the language of input text.
    """

    def __init__(self):
        self.supported_languages = set(SUPPORTED_LANGUAGES)

    def detect_language(self, request: LanguageDetectionRequest) -> LanguageDetectionResponse:
        """
        Detect the language of the input text.

        Args:
            request: LanguageDetectionRequest containing the text to analyze

        Returns:
            LanguageDetectionResponse with detected language and metadata
        """
        try:
            # Detect the most likely language
            detected_language = detect(request.text)

            # Get all possible language matches with confidence scores
            all_language_probs = detect_langs(request.text)

            # Filter to only supported languages if needed
            all_matches = []
            for lang_prob in all_language_probs:
                lang_code = lang_prob.lang
                confidence = lang_prob.prob

                # Create LanguageMatch object
                match = LanguageMatch(
                    language=lang_code,
                    confidence=confidence
                )
                all_matches.append(match)

            # Get the primary detected language (highest confidence)
            primary_match = all_language_probs[0] if all_language_probs else None
            primary_language = primary_match.lang if primary_match else detected_language
            primary_confidence = primary_match.prob if primary_match else 0.0

            # Create response
            response = LanguageDetectionResponse(
                detected_language=primary_language,
                confidence=primary_confidence,
                all_matches=all_matches if all_matches else None,
                char_count=len(request.text)
            )

            return response

        except Exception as e:
            raise LanguageDetectionError(f"Language detection failed: {str(e)}")