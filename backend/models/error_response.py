from pydantic import BaseModel, Field
from typing import Optional, Dict, Any


class ErrorResponse(BaseModel):
    """
    Error response model for API errors.

    Based on the API contract specification.
    """
    error: str = Field(
        ...,
        description="Error code",
        example="TRANSLATION_ERROR"
    )
    message: str = Field(
        ...,
        description="Human-readable error message",
        example="Translation service unavailable"
    )
    details: Optional[Dict[str, Any]] = Field(
        None,
        description="Additional error details",
        example={"api_limit": "Rate limit exceeded, please try again later"}
    )