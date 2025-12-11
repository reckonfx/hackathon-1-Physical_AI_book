import requests
from typing import Dict, Any
from backend.config import TRANSLATION_API_KEY, DETECTION_API_URL
from backend.exceptions import TranslationAPIError, RateLimitExceededError


class LanguageDetectionApiClient:
    """
    Client for interacting with external language detection APIs.
    """

    def __init__(self):
        self.api_key = TRANSLATION_API_KEY
        self.api_url = DETECTION_API_URL
        self.session = requests.Session()
        if self.api_key:
            self.session.headers.update({"X-API-Key": self.api_key})

    def detect_language(self, text: str) -> Dict[str, Any]:
        """
        Detect language of text using the external API.

        Args:
            text: Text to analyze for language detection

        Returns:
            Dictionary containing language detection result
        """
        # Prepare request payload
        payload = {
            "q": text
        }

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
            detected_info = self._extract_language_info(result)

            return detected_info

        except requests.exceptions.RequestException as e:
            raise TranslationAPIError(f"Request failed: {str(e)}")
        except KeyError as e:
            raise TranslationAPIError(f"Unexpected API response format: {str(e)}")
        except Exception as e:
            raise TranslationAPIError(f"Language detection failed: {str(e)}")

    def _extract_language_info(self, api_response: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract language information from API response based on the service format.
        This method should be customized based on the specific API being used.
        """
        # This is a generic extraction - customize based on the actual API response format
        # For example, Google Translate API format might be different
        if "data" in api_response and "detections" in api_response["data"]:
            # Google Translate API format
            detections = api_response["data"]["detections"][0]  # First detection
            primary_detection = detections[0]  # Most confident detection
            return {
                "language": primary_detection["language"],
                "confidence": primary_detection.get("confidence", 0.0),
                "isReliable": primary_detection.get("isReliable", False)
            }
        elif "language" in api_response:
            # Direct format
            return {
                "language": api_response["language"],
                "confidence": api_response.get("confidence", 0.0),
                "isReliable": api_response.get("isReliable", False)
            }
        else:
            # Fallback: try to find language info in response
            for key, value in api_response.items():
                if isinstance(value, dict) and "language" in value:
                    return value
            raise TranslationAPIError("Could not extract language info from API response")