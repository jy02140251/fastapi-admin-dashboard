"""
Application Configuration Module.

Loads settings from environment variables with sensible defaults.
Uses pydantic-settings for type-safe configuration management.
"""

from typing import List

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Project
    PROJECT_NAME: str = "FastAPI Admin Dashboard"
    DEBUG: bool = False
    API_V1_PREFIX: str = "/api/v1"

    # Database
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/admin_dashboard"

    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"

    # JWT Configuration
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # CORS
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
    ]

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()