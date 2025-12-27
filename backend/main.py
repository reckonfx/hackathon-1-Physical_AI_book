from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging
import os

try:
    # When running as a module (e.g., uvicorn main:app)
    from .api.v1.rag_router import router as rag_router
    from .api.v1.chat_router import router as chat_router
    from .api.v1.health_router import router as health_router
except ImportError:
    # When running directly
    from api.v1.rag_router import router as rag_router
    from api.v1.chat_router import router as chat_router
    from api.v1.health_router import router as health_router

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan events for the FastAPI application.
    This runs startup and shutdown logic.
    """
    logger.info("Starting up the RAG API application...")
    # Initialize resources here (e.g., database connections, vector stores)
    yield
    logger.info("Shutting down the RAG API application...")
    # Cleanup resources here if needed

# Create FastAPI app with lifespan
app = FastAPI(
    title="Physical AI Book RAG API",
    description="API for retrieval-augmented generation functionality for the Physical AI Book",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health_router, prefix="/api", tags=["health"])
app.include_router(rag_router, prefix="/api", tags=["rag"])
app.include_router(chat_router, prefix="/api", tags=["chat"])

# Root endpoint
@app.get("/")
async def root():
    return {"message": "Physical AI Book RAG API", "version": "1.0.0"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)