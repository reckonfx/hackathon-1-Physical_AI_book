# Research: OpenRouter Chatbot Migration

## Decision: OpenRouter API Configuration
**Rationale**: OpenRouter provides an OpenAI-compatible API that allows us to use the existing LangChain OpenAI integration with minimal code changes. By configuring the base URL and API key, we can maintain the same interface while switching to OpenRouter's models.
**Alternatives considered**:
- Complete rewrite to use OpenRouter's specific SDK (would require significant code changes)
- Separate OpenRouter-specific service (would add complexity and duplicate functionality)

## Decision: Model Selection
**Rationale**: Using `meta-llama/llama-3-8b-instruct` as the default model provides good performance for the book content while being cost-effective on OpenRouter. The model can be configured via environment variable for flexibility.
**Alternatives considered**:
- Other models like `gpt-3.5-turbo` (already used in current implementation)
- OpenRouter's recommended models for RAG applications

## Decision: Error Handling Approach
**Rationale**: Maintaining the existing error handling structure while adding specific OpenRouter error logging will preserve the user experience while providing better developer visibility into API issues.
**Alternatives considered**:
- Adding new error handling mechanisms (would complicate the codebase)
- Removing error handling entirely (would make debugging difficult)

## Decision: Embedding Strategy
**Rationale**: Since the current implementation already has fallback logic between Google embeddings and OpenAI embeddings, we can maintain the same fallback behavior. If OpenAI embeddings are used, they will continue to work with OpenRouter's endpoint.
**Alternatives considered**:
- Switching to OpenRouter-compatible embeddings (would require additional configuration)
- Using local embeddings only (would reduce quality)

## Technical Findings

1. **Current Architecture**: The system uses LangChain with `ChatOpenAI` and `OpenAIEmbeddings` classes
2. **API Key Availability**: OpenRouter API key is already present in the backend `.env` file
3. **RAG Pipeline**: FAISS vector stores are used for similarity search, with content loaded from markdown files
4. **Service Structure**: `ai_agent_rag_service.py` handles the main RAG functionality
5. **Environment Configuration**: The system uses a Settings class in `config.py` to manage environment variables
6. **Fallback Logic**: The current system has fallback logic between Google and OpenAI models/embeddings