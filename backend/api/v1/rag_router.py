from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import logging

try:
    # When running as a module
    from ...models.rag_models import SearchRequest, SearchResponse, SearchResult, ValidateContentRequest, ValidateContentResponse
    from ...services.rag_service import RAGService
except ImportError:
    # When running directly for testing
    import sys
    import os
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
    from models.rag_models import SearchRequest, SearchResponse, SearchResult, ValidateContentRequest, ValidateContentResponse
    from services.rag_service import RAGService

router = APIRouter()
logger = logging.getLogger(__name__)

# Initialize the RAG service
rag_service = RAGService()

class ContentChunk(BaseModel):
    content: str
    source: str
    score: float
    chunk_size: int

@router.post("/search", response_model=SearchResponse)
async def search_content(request: SearchRequest):
    """
    Search book content for relevant passages
    """
    try:
        logger.info(f"Received search request: {request.query[:50]}...")

        # Perform the search using the RAG service
        results = await rag_service.search(
            query=request.query,
            max_results=request.max_results or 5,
            module_filter=request.module_filter
        )

        logger.info(f"Found {len(results)} results for query: {request.query[:30]}...")
        return SearchResponse(results=results)

    except Exception as e:
        logger.error(f"Error during search: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")

@router.post("/validate-content", response_model=ValidateContentResponse)
async def validate_content(request: ValidateContentRequest):
    """
    Validate content for RAG optimization
    """
    try:
        logger.info(f"Validating content of size {len(request.content)} characters")

        # Validate the content using the RAG service
        is_valid, suggestions, chunk_size = await rag_service.validate_content(
            content=request.content,
            min_chunk_size=request.min_chunk_size,
            max_chunk_size=request.max_chunk_size
        )

        logger.info(f"Content validation completed. Valid: {is_valid}")
        return ValidateContentResponse(
            is_valid=is_valid,
            suggestions=suggestions,
            chunk_size=chunk_size
        )

    except Exception as e:
        logger.error(f"Error during content validation: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Validation failed: {str(e)}")