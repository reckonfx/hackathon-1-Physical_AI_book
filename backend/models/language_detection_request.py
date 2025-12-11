from pydantic import BaseModel, Field
from typing import Optional


class LanguageDetectionRequest(BaseModel):
    """
    Request model for language detection.

    Based on the data model specification and API contract.
    """
    text: str = Field(
        ...,
        description="The text to analyze for language detection (max 1000 characters)",
        max_length=1000,
        example="The robot moved through the environment using SLAM algorithms."
    )