from typing import List, Dict
from backend.models.translation_request import TranslationRequest
from backend.models.translation_response import TranslationResponse
from backend.services.translation_service import TranslationService
from backend.config import SUPPORTED_LANGUAGES


class BatchTranslationService:
    """
    Service for performing batch translation to multiple target languages.
    """

    def __init__(self):
        self.translation_service = TranslationService()

    def translate_to_multiple_languages(
        self,
        text: str,
        target_languages: List[str],
        source_language: str = None,
        preserve_formatting: bool = True,
        glossary_ref: bool = False
    ) -> Dict[str, TranslationResponse]:
        """
        Translate text to multiple target languages in a batch operation.

        Args:
            text: The text to translate
            target_languages: List of target language codes
            source_language: Source language code (optional, will auto-detect if not provided)
            preserve_formatting: Whether to preserve formatting
            glossary_ref: Whether to include glossary references

        Returns:
            Dictionary mapping language codes to their translation responses
        """
        results = {}

        for target_lang in target_languages:
            # Validate target language
            if target_lang not in SUPPORTED_LANGUAGES:
                # Skip unsupported languages or raise an error depending on requirements
                continue

            # Create a translation request for this specific target language
            request = TranslationRequest(
                text=text,
                target_language=target_lang,
                source_language=source_language,
                preserve_formatting=preserve_formatting,
                glossary_ref=glossary_ref
            )

            try:
                # Perform the translation
                response = self.translation_service.translate(request)
                results[target_lang] = response
            except Exception as e:
                # In a real implementation, you might want to continue with other languages
                # or return error information for this specific language
                # For now, we'll skip failed translations
                print(f"Translation to {target_lang} failed: {str(e)}")
                continue

        return results

    def translate_to_all_supported_languages(
        self,
        text: str,
        source_language: str = None,
        preserve_formatting: bool = True,
        glossary_ref: bool = False
    ) -> Dict[str, TranslationResponse]:
        """
        Translate text to all supported languages.

        Args:
            text: The text to translate
            source_language: Source language code (optional)
            preserve_formatting: Whether to preserve formatting
            glossary_ref: Whether to include glossary references

        Returns:
            Dictionary mapping language codes to their translation responses
        """
        return self.translate_to_multiple_languages(
            text=text,
            target_languages=SUPPORTED_LANGUAGES,
            source_language=source_language,
            preserve_formatting=preserve_formatting,
            glossary_ref=glossary_ref
        )