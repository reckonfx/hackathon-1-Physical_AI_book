from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class HealthCheck(BaseModel):
    status: str = "healthy"
    version: str = "1.0.0"

@router.get("/health", response_model=HealthCheck)
async def health_check():
    return HealthCheck()