"""
Aura Camera App - Python ML API
FastAPI backend for face detection, biofeedback processing, and aura generation
"""

import os
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import JSONResponse

from api.routes import aura_generation, biofeedback, face_detection, health, reading_generation
from config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler"""
    # Startup
    print("Starting Aura Camera ML API...")
    print(f"Environment: {settings.ENVIRONMENT}")
    print(f"Debug Mode: {settings.DEBUG}")
    
    yield
    
    # Shutdown
    print("Shutting down Aura Camera ML API...")


# Create FastAPI application
app = FastAPI(
    title="Aura Camera ML API",
    description="Machine Learning API for Aura Camera App - Face detection, biofeedback processing, and aura generation",
    version="1.0.0",
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None,
    lifespan=lifespan,
)

# Add middleware
app.add_middleware(GZipMiddleware, minimum_size=1000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Exception handlers
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler"""
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": {
                "code": "INTERNAL_ERROR",
                "message": "An internal error occurred" if not settings.DEBUG else str(exc),
            },
        },
    )


# Include routers
app.include_router(health.router, prefix="/health", tags=["Health"])
app.include_router(face_detection.router, prefix="/face-detection", tags=["Face Detection"])
app.include_router(biofeedback.router, prefix="/biofeedback", tags=["Biofeedback"])
app.include_router(aura_generation.router, prefix="/aura", tags=["Aura Generation"])
app.include_router(reading_generation.router, prefix="/reading", tags=["Reading Generation"])


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "name": "Aura Camera ML API",
        "version": "1.0.0",
        "status": "running",
        "environment": settings.ENVIRONMENT,
    }


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        workers=1 if settings.DEBUG else 4,
    )
