from fastapi import APIRouter, HTTPException
from typing import List
import logging

try:
    # When running as a module
    from ...models.chat_models import ChatMessage, ChatRequest, ChatResponse
    from ...services.chatbot_service import ChatbotService
except ImportError:
    # When running directly for testing
    import sys
    import os
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
    from models.chat_models import ChatMessage, ChatRequest, ChatResponse
    from services.chatbot_service import ChatbotService

router = APIRouter()
logger = logging.getLogger(__name__)

# Initialize the chatbot service
chatbot_service = ChatbotService()

@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """
    Chat endpoint that uses RAG to answer questions about the Physical AI book
    """
    try:
        logger.info(f"Received chat request with {len(request.messages)} messages")

        # Initialize the chatbot service if not already done
        await chatbot_service.initialize()

        # Process the chat request
        response = await chatbot_service.chat(request)

        logger.info(f"Generated chat response with {len(response.sources)} sources")
        return response

    except Exception as e:
        error_msg = str(e).lower()
        logger.error(f"Error during chat: {str(e)}")
        # More specific error handling for OpenRouter API errors
        if "openrouter" in error_msg or "api" in error_msg or "authentication" in error_msg or "401" in error_msg or "403" in error_msg:
            logger.error(f"OpenRouter API error: {str(e)}")
            raise HTTPException(status_code=500, detail="AI service is temporarily unavailable. Please try again later.")
        elif "rate limit" in error_msg or "quota" in error_msg:
            logger.error(f"OpenRouter rate limit error: {str(e)}")
            raise HTTPException(status_code=500, detail="AI service is temporarily unavailable due to high demand. Please try again later.")
        else:
            raise HTTPException(status_code=500, detail=f"Chat failed: {str(e)}")

@router.post("/chat/stream")
async def chat_stream_endpoint(request: ChatRequest):
    """
    Streaming chat endpoint (placeholder for future implementation)
    """
    try:
        await chatbot_service.initialize()
        response = await chatbot_service.chat(request)

        # In a real implementation, this would stream the response
        # For now, return the complete response
        yield response.model_dump()
    except Exception as e:
        error_msg = str(e).lower()
        logger.error(f"Error during streaming chat: {str(e)}")
        # More specific error handling for OpenRouter API errors
        if "openrouter" in error_msg or "api" in error_msg or "authentication" in error_msg or "401" in error_msg or "403" in error_msg:
            logger.error(f"OpenRouter API error: {str(e)}")
            raise HTTPException(status_code=500, detail="AI service is temporarily unavailable. Please try again later.")
        elif "rate limit" in error_msg or "quota" in error_msg:
            logger.error(f"OpenRouter rate limit error: {str(e)}")
            raise HTTPException(status_code=500, detail="AI service is temporarily unavailable due to high demand. Please try again later.")
        else:
            raise HTTPException(status_code=500, detail=f"Streaming chat failed: {str(e)}")