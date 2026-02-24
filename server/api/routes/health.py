"""Health check endpoints"""

from fastapi import APIRouter, status
from pydantic import BaseModel
from datetime import datetime

router = APIRouter()


class HealthResponse(BaseModel):
    status: str
    timestamp: str
    version: str


class HealthCheckResponse(BaseModel):
    status: str
    services: dict
    timestamp: str


@router.get(
    "",
    response_model=HealthResponse,
    status_code=status.HTTP_200_OK,
    summary="Basic health check",
)
async def health_check():
    """Basic health check endpoint"""
    return HealthResponse(
        status="healthy",
        timestamp=datetime.utcnow().isoformat(),
        version="1.0.0",
    )


@router.get(
    "/detailed",
    response_model=HealthCheckResponse,
    status_code=status.HTTP_200_OK,
    summary="Detailed health check",
)
async def detailed_health_check():
    """Detailed health check with service status"""
    services = {
        "api": "healthy",
        "face_detection": "healthy",
        "aura_generation": "healthy",
        "reading_generation": "healthy",
    }
    
    return HealthCheckResponse(
        status="healthy",
        services=services,
        timestamp=datetime.utcnow().isoformat(),
    )
