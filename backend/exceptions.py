class TranslationError(Exception):
    """Base exception for translation-related errors."""
    def __init__(self, message: str, error_code: str = "TRANSLATION_ERROR"):
        self.message = message
        self.error_code = error_code
        super().__init__(self.message)


class LanguageDetectionError(Exception):
    """Base exception for language detection-related errors."""
    def __init__(self, message: str, error_code: str = "LANGUAGE_DETECTION_ERROR"):
        self.message = message
        self.error_code = error_code
        super().__init__(self.message)


class UnsupportedLanguageError(TranslationError):
    """Exception raised when an unsupported language is requested."""
    def __init__(self, language_code: str):
        self.language_code = language_code
        super().__init__(
            f"Unsupported language code: {language_code}",
            "UNSUPPORTED_LANGUAGE"
        )


class CharacterLimitExceededError(TranslationError):
    """Exception raised when input text exceeds character limit."""
    def __init__(self, char_count: int, limit: int):
        self.char_count = char_count
        self.limit = limit
        super().__init__(
            f"Character limit exceeded: {char_count} characters provided, limit is {limit}",
            "CHARACTER_LIMIT_EXCEEDED"
        )


class TranslationAPIError(TranslationError):
    """Exception raised when translation API returns an error."""
    def __init__(self, message: str, api_error_code: str = None):
        self.api_error_code = api_error_code
        super().__init__(
            f"Translation API error: {message}",
            "TRANSLATION_API_ERROR"
        )


class RateLimitExceededError(TranslationError):
    """Exception raised when rate limit is exceeded."""
    def __init__(self, message: str = "Rate limit exceeded, please try again later"):
        super().__init__(
            message,
            "RATE_LIMIT_EXCEEDED"
        )


class ErrorResponse:
    """Error response model for API errors."""
    def __init__(self, error: str, message: str, details: dict = None):
        self.error = error
        self.message = message
        self.details = details or {}