from fastapi import APIRouter, HTTPException, Depends, Request
from typing import Optional
import time

from backend.models.translation_request import TranslationRequest
from backend.models.translation_response import TranslationResponse
from backend.models.error_response import ErrorResponse
from backend.services.translation_service import TranslationService
from backend.middleware.rate_limit import rate_limit_middleware
from backend.exceptions import (
    TranslationError,
    UnsupportedLanguageError,
    CharacterLimitExceededError,
    RateLimitExceededError
)

router = APIRouter(prefix="/translate", tags=["translation"])

# Initialize services
translation_service = TranslationService()


@router.post("/", response_model=TranslationResponse)
async def translate_text(
    request: Request,
    translation_request: TranslationRequest,
    x_api_key: Optional[str] = None  # For API key header
):
    """
    Translate text to the specified target language.
    """
    # Apply rate limiting
    try:
        rate_limit_middleware(request)
    except HTTPException:
        raise HTTPException(
            status_code=429,
            detail="Rate limit exceeded. Please try again later."
        )

    try:
        # Perform translation
        start_time = time.time()
        result = translation_service.translate(translation_request)
        processing_time = (time.time() - start_time) * 1000

        # Update processing time with actual time taken by service + endpoint
        result.processing_time += processing_time

        return result
    except UnsupportedLanguageError as e:
        raise HTTPException(
            status_code=400,
            detail={
                "error": e.error_code,
                "message": e.message,
                "details": {"language_code": e.language_code}
            }
        )
    except CharacterLimitExceededError as e:
        raise HTTPException(
            status_code=400,
            detail={
                "error": e.error_code,
                "message": e.message,
                "details": {
                    "char_count": e.char_count,
                    "limit": e.limit
                }
            }
        )
    except RateLimitExceededError as e:
        raise HTTPException(
            status_code=429,
            detail={
                "error": e.error_code,
                "message": e.message
            }
        )
    except TranslationError as e:
        raise HTTPException(
            status_code=500,
            detail={
                "error": e.error_code,
                "message": e.message
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "error": "INTERNAL_ERROR",
                "message": f"An unexpected error occurred: {str(e)}"
            }
        )


# Add the API key dependency if needed
def require_api_key(x_api_key: str = None):
    # In a real implementation, you would validate the API key here
    # For now, we'll just check if it exists
    if not x_api_key:
        raise HTTPException(
            status_code=401,
            detail="API key is required"
        )
    # Here you would typically validate the key against a database or configuration
    # For this implementation, we'll assume any non-empty key is valid
    return x_api_key