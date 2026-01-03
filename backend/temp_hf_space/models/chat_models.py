from pydantic import BaseModel
from typing import List, Optional

class ChatMessage(BaseModel):
    role: str  # "user", "assistant", or "system"
    content: str

class ChatRequest(BaseModel):
    messages: List[ChatMessage]
    max_results: int = 5
    temperature: float = 0.7
    module_filter: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    sources: List[str]
    tokens_used: int