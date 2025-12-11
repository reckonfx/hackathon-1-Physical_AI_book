from typing import List
from backend.config import SUPPORTED_LANGUAGES
from backend.exceptions import UnsupportedLanguageError


def validate_language_code(language_code: str) -> bool:
    """
    Validate if a language code is supported.

    Args:
        language_code: The language code to validate (ISO 639-1 format)

    Returns:
        True if the language code is supported, False otherwise
    """
    if not language_code or len(language_code) != 2 or not language_code.isalpha() or not language_code.islower():
        return False

    return language_code in SUPPORTED_LANGUAGES


def validate_language_codes(language_codes: List[str]) -> List[str]:
    """
    Validate a list of language codes and return only the supported ones.

    Args:
        language_codes: List of language codes to validate

    Returns:
        List of supported language codes
    """
    supported = []
    for code in language_codes:
        if validate_language_code(code):
            supported.append(code)
    return supported


def get_supported_languages() -> List[str]:
    """
    Get the list of supported languages.

    Returns:
        List of supported language codes
    """
    return SUPPORTED_LANGUAGES.copy()


def validate_and_raise(language_code: str) -> None:
    """
    Validate a language code and raise an exception if not supported.

    Args:
        language_code: The language code to validate

    Raises:
        UnsupportedLanguageError: If the language code is not supported
    """
    if not validate_language_code(language_code):
        raise UnsupportedLanguageError(language_code)