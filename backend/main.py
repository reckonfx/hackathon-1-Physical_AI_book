from fastapi import FastAPI
from backend.api.v1.translator import router as translator_router
from backend.api.v1.language_detector import router as language_detector_router
from backend.utils.logger import TranslationLogger
from backend.utils.performance_monitor import performance_monitor
import time


# Initialize logger
logger = TranslationLogger("translator-agent")

# Create FastAPI app
app = FastAPI(
    title="TranslatorAgent API",
    description="API for translating book content to different languages",
    version="1.0.0"
)

# Include API routers
app.include_router(
    translator_router,
    prefix="/api/v1",
    tags=["translation"]
)

app.include_router(
    language_detector_router,
    prefix="/api/v1",
    tags=["language-detection"]
)


@app.get("/")
async def root():
    """Root endpoint for health check."""
    return {"message": "TranslatorAgent API is running", "status": "healthy"}


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "TranslatorAgent",
        "version": "1.0.0",
        "timestamp": time.time(),
        "uptime": time.time() - getattr(health_check, 'start_time', time.time()),
        "checks": {
            "api_availability": "ok",
            "translation_service": "ok",  # Would check actual service status in production
            "language_detection_service": "ok"  # Would check actual service status in production
        }
    }

# Set start time for uptime calculation
health_check.start_time = time.time()


@app.get("/metrics")
async def get_metrics():
    """Performance metrics endpoint."""
    return {
        "performance": performance_monitor.get_stats(),
        "timestamp": time.time()
    }


# Add middleware for logging and performance monitoring
@app.middleware("http")
async def log_and_monitor(request, call_next):
    start_time = time.time()
    request_id = f"{time.time()}-{id(request)}"  # Simple request ID

    # Log the request
    if request.method in ["POST"] and "translate" in request.url.path:
        body_bytes = await request.body()
        # Note: This is a simplified approach - in production, you might want
        # to handle this differently to avoid reading the body twice
        pass

    # Monitor performance
    performance_monitor.start_timer(request_id, request.url.path)

    response = await call_next(request)

    # End performance monitoring
    elapsed_ms = performance_monitor.end_timer(request_id, request.url.path)

    # Log the response
    logger.log_translation_response(
        {"endpoint": request.url.path, "status_code": response.status_code},
        elapsed_ms or (time.time() - start_time) * 1000
    )

    return response


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)