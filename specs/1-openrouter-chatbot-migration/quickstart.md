# Quickstart: OpenRouter Chatbot Migration

## Prerequisites

- Python 3.11+
- Node.js (for frontend, if applicable)
- OpenRouter API key (already configured in `.env`)

## Setup

1. **Environment Configuration**
   - Verify `OPENROUTER_API_KEY` is set in `backend/.env`
   - Set `OPENROUTER_MODEL` to desired model (defaults to `meta-llama/llama-3-8b-instruct`)

2. **Install Dependencies**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

3. **Start Services**
   ```bash
   cd backend
   uvicorn main:app --reload
   ```

## Configuration

### Environment Variables

Add to your `.env` file:
```env
OPENROUTER_API_KEY=your-openrouter-api-key
OPENROUTER_MODEL=meta-llama/llama-3-8b-instruct
```

### Model Configuration

The system will automatically use OpenRouter when:
- `OPENROUTER_API_KEY` is present
- OpenAI configuration is updated to use OpenRouter endpoint

## API Endpoints

- `POST /api/chat` - Main chat endpoint with RAG functionality
- `POST /api/chat/stream` - Streaming chat endpoint (placeholder)

## Testing

1. **Verify API Key Loading**:
   - Check that the OpenRouter API key is loaded at startup
   - Verify no OpenAI API key errors

2. **Test Chat Functionality**:
   ```bash
   curl -X POST http://localhost:8000/api/chat \
     -H "Content-Type: application/json" \
     -d '{
       "messages": [{"role": "user", "content": "Hello"}],
       "max_results": 5
     }'
   ```

3. **Verify RAG Functionality**:
   - Test that document retrieval still works
   - Confirm responses are context-aware

## Troubleshooting

- **API Key Errors**: Ensure `OPENROUTER_API_KEY` is properly set
- **Model Not Found**: Verify the model name is supported by OpenRouter
- **RAG Issues**: Check that FAISS vector stores are loading correctly