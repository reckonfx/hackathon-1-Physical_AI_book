from pydantic import BaseModel, Field
from typing import Optional, List


class TranslationResponse(BaseModel):
    """
    Response model for text translation.

    Based on the data model specification and API contract.
    """
    translated_text: str = Field(
        ...,
        description="The translated text content",
        example="El robot se movió a través del entorno utilizando algoritmos SLAM."
    )
    detected_source_language: Optional[str] = Field(
        None,
        description="The detected source language code (ISO 639-1)",
        pattern=r"^[a-z]{2}$",
        example="en"
    )
    target_language: str = Field(
        ...,
        description="The target language code (ISO 639-1)",
        pattern=r"^[a-z]{2}$",
        example="es"
    )
    confidence: Optional[float] = Field(
        None,
        description="Confidence score of the translation (0-1)",
        ge=0,
        le=1,
        example=0.92
    )
    technical_terms: Optional[List[str]] = Field(
        None,
        description="List of technical terms preserved in original form",
        example=["SLAM", "robot"]
    )
    char_count: int = Field(
        ...,
        description="Character count of original text",
        example=54
    )
    processing_time: float = Field(
        ...,
        description="Time taken to process the request in milliseconds",
        example=1250.0
    )