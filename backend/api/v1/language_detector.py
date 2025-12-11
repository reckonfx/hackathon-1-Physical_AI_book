from fastapi import APIRouter, HTTPException, Request
from typing import Optional

from backend.models.language_detection_request import LanguageDetectionRequest
from backend.models.language_detection_response import LanguageDetectionResponse
from backend.services.language_detection_service import LanguageDetectionService
from backend.middleware.rate_limit import rate_limit_middleware
from backend.exceptions import LanguageDetectionError, RateLimitExceededError

router = APIRouter(prefix="/detect-language", tags=["language-detection"])

# Initialize service
language_detection_service = LanguageDetectionService()


@router.post("/", response_model=LanguageDetectionResponse)
async def detect_language(
    request: Request,
    detection_request: LanguageDetectionRequest,
    x_api_key: Optional[str] = None  # For API key header
):
    """
    Detect the language of the provided text.
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
        # Perform language detection
        result = language_detection_service.detect_language(detection_request)
        return result
    except RateLimitExceededError as e:
        raise HTTPException(
            status_code=429,
            detail={
                "error": e.error_code,
                "message": e.message
            }
        )
    except LanguageDetectionError as e:
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