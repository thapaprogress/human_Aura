"""Application configuration"""

from typing import List

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings"""
    
    # Application
    APP_NAME: str = "Aura Camera ML API"
    APP_VERSION: str = "1.0.0"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    
    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # CORS
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:3001",
        "https://auracamera.app",
        "https://www.auracamera.app",
    ]
    
    # Database
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/aura_camera"
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379"
    
    # JWT
    JWT_SECRET: str = "your-secret-key-change-in-production"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRES_IN: int = 7 * 24 * 60 * 60  # 7 days
    
    # Cloudinary
    CLOUDINARY_CLOUD_NAME: str = ""
    CLOUDINARY_API_KEY: str = ""
    CLOUDINARY_API_SECRET: str = ""
    
    # OpenAI
    OPENAI_API_KEY: str = ""
    
    # Face Detection
    FACE_DETECTION_CONFIDENCE: float = 0.5
    FACE_TRACKING_CONFIDENCE: float = 0.5
    
    # Aura Generation
    AURA_DEFAULT_STYLE: str = "soft"
    AURA_BLUR_KERNEL_SIZE: int = 51
    
    # Biofeedback
    BIOFEEDBACK_SAMPLE_RATE: int = 30
    BIOFEEDBACK_MIN_DURATION: int = 5000  # milliseconds
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Global settings instance
settings = Settings()
