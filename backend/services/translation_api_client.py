import requests
import time
from typing import Dict, Any, Optional
from backend.config import TRANSLATION_API_KEY, TRANSLATION_API_URL
from backend.exceptions import TranslationAPIError, RateLimitExceededError


class TranslationApiClient:
    """
    Client for interacting with external translation APIs.
    """

    def __init__(self):
        self.api_key = TRANSLATION_API_KEY
        self.api_url = TRANSLATION_API_URL
        self.session = requests.Session()
        if self.api_key:
            self.session.headers.update({"X-API-Key": self.api_key})

    def translate_text(
        self,
        text: str,
        target_language: str,
        source_language: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Translate text using the external translation API.

        Args:
            text: Text to translate
            target_language: Target language code
            source_language: Source language code (optional, will auto-detect if not provided)

        Returns:
            Dictionary containing translation result
        """
        # Prepare request payload
        payload = {
            "q": text,
            "target": target_language,
        }

        if source_language:
            payload["source"] = source_language

        # Add API key if using Google Translate or similar
        if self.api_key:
            payload["key"] = self.api_key

        try:
            response = self.session.post(self.api_url, json=payload, timeout=30)

            if response.status_code == 429:
                raise RateLimitExceededError()

            response.raise_for_status()

            result = response.json()

            # Process the result based on the API format
            # This is a generic implementation - adjust based on the specific API response format
            translated_text = self._extract_translated_text(result)

            return {
                "translated_text": translated_text,
                "source_language": source_language or result.get("detectedSourceLanguage"),
                "target_language": target_language,
                "confidence": result.get("confidence", 0.8)  # Default confidence
            }

        except requests.exceptions.RequestException as e:
            raise TranslationAPIError(f"Request failed: {str(e)}")
        except KeyError as e:
            raise TranslationAPIError(f"Unexpected API response format: {str(e)}")
        except Exception as e:
            raise TranslationAPIError(f"Translation failed: {str(e)}")

    def _extract_translated_text(self, api_response: Dict[str, Any]) -> str:
        """
        Extract translated text from API response based on the service format.
        This method should be customized based on the specific translation API being used.
        """
        # This is a generic extraction - customize based on the actual API response format
        # For example, Google Translate API format might be different
        if "data" in api_response and "translations" in api_response["data"]:
            # Google Translate API format
            return api_response["data"]["translations"][0].get("translatedText", "")
        elif "translatedText" in api_response:
            # Direct format
            return api_response["translatedText"]
        else:
            # Fallback: try to find translated text in response
            for key, value in api_response.items():
                if isinstance(value, str) and len(value) > 0:
                    return value
            raise TranslationAPIError("Could not extract translated text from API response")