from pydantic import BaseModel, Field, validator
from typing import Optional


class TranslationRequest(BaseModel):
    """
    Request model for text translation.

    Based on the data model specification and API contract.
    """
    text: str = Field(
        ...,
        description="The source text to be translated (max 1000 characters)",
        max_length=1000,
        example="The robot moved through the environment using SLAM algorithms."
    )
    target_language: str = Field(
        ...,
        description="The language code to translate to (ISO 639-1)",
        pattern=r"^[a-z]{2}$",
        example="es"
    )
    source_language: Optional[str] = Field(
        None,
        description="The language code of the source text (ISO 639-1), if not provided auto-detect",
        pattern=r"^[a-z]{2}$",
        example="en"
    )
    preserve_formatting: Optional[bool] = Field(
        True,
        description="Whether to attempt to preserve original formatting"
    )
    glossary_ref: Optional[bool] = Field(
        False,
        description="Whether to include glossary references for technical terms"
    )

    @validator('target_language')
    def validate_target_language(cls, v):
        # Basic validation for ISO 639-1 language codes
        if not v or len(v) != 2 or not v.isalpha() or not v.islower():
            raise ValueError('target_language must be a valid ISO 639-1 language code (2 lowercase letters)')
        return v

    @validator('source_language', pre=True)
    def validate_source_language(cls, v):
        if v is None:
            return v
        if not v or len(v) != 2 or not v.isalpha() or not v.islower():
            raise ValueError('source_language must be a valid ISO 639-1 language code (2 lowercase letters)')
        return v