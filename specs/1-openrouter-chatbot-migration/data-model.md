# Data Model: OpenRouter Chatbot Migration

## Entities

### ChatMessage
**Description**: Represents a single message in a chat conversation
**Fields**:
- role: string (user, assistant, system)
- content: string (the message content)

### ChatRequest
**Description**: Request object for chat API calls
**Fields**:
- messages: List[ChatMessage] (conversation history)
- max_results: int (number of RAG results to retrieve)
- module_filter: Optional[string] (filter for specific book modules)

### ChatResponse
**Description**: Response object from chat API
**Fields**:
- response: string (the AI-generated response)
- sources: List[string] (list of source documents used)
- tokens_used: int (approximate token count)

### SearchResult
**Description**: Result from RAG search operations
**Fields**:
- content: string (retrieved content snippet)
- source: string (source document identifier)
- score: float (relevance score)
- chunk_size: int (size of the content chunk)

## Relationships

- ChatRequest contains multiple ChatMessage objects
- ChatResponse contains multiple source strings from SearchResult objects
- SearchResult objects are generated during RAG search process

## Validation Rules

- ChatMessage role must be one of: "user", "assistant", "system"
- ChatRequest must contain at least one user message
- SearchResult content must be non-empty when returned