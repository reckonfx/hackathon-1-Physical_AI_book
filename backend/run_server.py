import uvicorn
from config import settings

def main():
    print(f"Starting Physical AI Book RAG API server...")
    print(f"Host: {settings.HOST}")
    print(f"Port: {settings.PORT}")
    print(f"Debug: {settings.DEBUG}")
    print(f"Content directory: {settings.CONTENT_DIR}")

    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level="info"
    )

if __name__ == "__main__":
    main()