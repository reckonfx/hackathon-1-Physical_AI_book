from pydantic import BaseModel
from typing import List, Optional

class SearchResult(BaseModel):
    content: str
    source: str
    score: float
    chunk_size: int

class SearchRequest(BaseModel):
    query: str
    max_results: Optional[int] = 5
    module_filter: Optional[str] = None

class SearchResponse(BaseModel):
    results: List[SearchResult]

class ValidateContentRequest(BaseModel):
    content: str
    min_chunk_size: int = 500
    max_chunk_size: int = 1200

class ValidateContentResponse(BaseModel):
    is_valid: bool
    suggestions: List[str]
    chunk_size: int