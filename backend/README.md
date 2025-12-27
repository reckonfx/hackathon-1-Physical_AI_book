# Physical AI Book RAG API

This is the backend API for the Physical AI & Humanoid Robotics book, providing retrieval-augmented generation (RAG) functionality to enable a chatbot that can answer questions about the book content. The system uses OpenRouter as the primary AI provider, with Google Gemini and OpenAI as fallback options.

## Architecture

The RAG API is built with FastAPI and provides:

1. **Search functionality** - Find relevant content from the book based on user queries
2. **Content validation** - Validate content chunks for proper RAG optimization
3. **Chat interface** - A chatbot that uses RAG to answer questions about the book content

## API Endpoints

### Health Check
- `GET /api/health` - Check API health status

### Search
- `POST /api/search` - Search book content for relevant passages
  - Request: `{"query": "search query", "max_results": 5, "module_filter": "optional module name"}`
  - Response: Array of search results with content, source, score, and chunk size

### Content Validation
- `POST /api/validate-content` - Validate content for RAG optimization
  - Request: `{"content": "content to validate", "min_chunk_size": 500, "max_chunk_size": 1200}`
  - Response: Validation result with suggestions

### Chat
- `POST /api/chat` - Chat with the RAG-enabled bot
  - Request: `{"messages": [{"role": "user", "content": "user message"}], "max_results": 5, "temperature": 0.7, "module_filter": "optional"}`
  - Response: Generated response with sources and token usage

## Implementation Details

### RAG Service
- Loads content from `book/docs/` directory
- Chunks content into 500-1200 character pieces
- Performs keyword-based search (with plans for embedding-based search)
- Provides content validation for proper RAG chunking

### Chatbot Service
- Integrates with RAG service to provide context
- Formats responses based on retrieved content
- Tracks sources for transparency
- Uses OpenRouter as primary AI provider, with Google Gemini and OpenAI as fallbacks
- Falls back to simulated responses when all AI providers are unavailable

## Running the API

### Prerequisites
- Python 3.10+
- Dependencies listed in `requirements.txt`

### Installation
```bash
pip install -r requirements.txt
```

### Running the Server
```bash
# From the project root directory
uvicorn backend.main:app --host 0.0.0.0 --port 8000
```

### Environment Variables
- `HOST` - Server host (default: 0.0.0.0)
- `PORT` - Server port (default: 8000)
- `DEBUG` - Debug mode (default: false)
- `CONTENT_DIR` - Content directory (default: book/docs)
- `MIN_CHUNK_SIZE` - Minimum chunk size for RAG (default: 500)
- `MAX_CHUNK_SIZE` - Maximum chunk size for RAG (default: 1200)

## Testing
Run the tests with:
```bash
python -m pytest backend/tests/
```

## Project Structure
```
backend/
├── main.py                 # FastAPI application entry point
├── config.py               # Configuration settings
├── run_server.py           # Server startup script
├── api/
│   └── v1/
│       ├── health_router.py # Health check endpoints
│       ├── rag_router.py    # RAG search endpoints
│       └── chat_router.py   # Chat endpoints
├── models/
│   ├── rag_models.py       # RAG-related data models
│   └── chat_models.py      # Chat-related data models
├── services/
│   ├── rag_service.py      # RAG service implementation
│   └── chatbot_service.py  # Chatbot service implementation
├── tests/
│   └── test_rag_api.py     # API tests
└── requirements.txt        # Dependencies
```

## Future Enhancements
- Integration with Qdrant vector database for semantic search
- Advanced content chunking strategies
- Caching for improved performance
- Authentication and rate limiting