from pydantic import BaseModel, Field
from typing import Optional, List


class LanguageMatch(BaseModel):
    """
    Model for a single language match with confidence score.
    """
    language: str = Field(
        ...,
        description="The language code (ISO 639-1)",
        pattern=r"^[a-z]{2}$",
        example="en"
    )
    confidence: float = Field(
        ...,
        description="Confidence score of the detection (0-1)",
        ge=0,
        le=1,
        example=0.98
    )


class LanguageDetectionResponse(BaseModel):
    """
    Response model for language detection.

    Based on the data model specification and API contract.
    """
    detected_language: str = Field(
        ...,
        description="The detected language code (ISO 639-1)",
        pattern=r"^[a-z]{2}$",
        example="en"
    )
    confidence: Optional[float] = Field(
        None,
        description="Confidence score of the detection (0-1)",
        ge=0,
        le=1,
        example=0.98
    )
    all_matches: Optional[List[LanguageMatch]] = Field(
        None,
        description="Array of all possible language matches with confidence scores"
    )
    char_count: int = Field(
        ...,
        description="Character count of input text",
        example=54
    )