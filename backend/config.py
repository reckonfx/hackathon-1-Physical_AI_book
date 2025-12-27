import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()  # Load from current directory
load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))  # Load from backend directory if exists

class Settings:
    """Application settings"""

    # API Configuration
    API_TITLE: str = "Physical AI Book RAG API"
    API_DESCRIPTION: str = "API for retrieval-augmented generation functionality for the Physical AI Book"
    API_VERSION: str = "1.0.0"

    # Server Configuration
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"

    # Content Configuration
    CONTENT_DIR: str = os.getenv("CONTENT_DIR", "book/docs")
    MIN_CHUNK_SIZE: int = int(os.getenv("MIN_CHUNK_SIZE", "500"))
    MAX_CHUNK_SIZE: int = int(os.getenv("MAX_CHUNK_SIZE", "1200"))

    # Vector Store Configuration (for future implementation)
    QDRANT_HOST: str = os.getenv("QDRANT_HOST", "localhost")
    QDRANT_PORT: int = int(os.getenv("QDRANT_PORT", "6333"))
    QDRANT_COLLECTION_NAME: str = os.getenv("QDRANT_COLLECTION_NAME", "book_content")

    # Model Configuration
    EMBEDDING_MODEL: str = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")
    LLM_MODEL: str = os.getenv("LLM_MODEL", "gpt-3.5-turbo")

    # API Keys
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")
    GOOGLE_API_KEY: Optional[str] = os.getenv("GOOGLE_API_KEY")
    OPENROUTER_API_KEY: Optional[str] = os.getenv("OPENROUTER_API_KEY")
    OPENROUTER_MODEL: str = os.getenv("OPENROUTER_MODEL", "meta-llama/llama-3-8b-instruct")

# Create a settings instance
settings = Settings()