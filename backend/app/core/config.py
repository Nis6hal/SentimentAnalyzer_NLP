"""
Configuration settings for SentimentIQ Backend.
Utilizes pydantic-settings to manage environment variables cleanly.
"""

from typing import List, Union
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import AnyHttpUrl, field_validator


class Settings(BaseSettings):
    PROJECT_NAME: str = "SentimentIQ"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # Database URL: defaults to local async SQLite for zero-friction run,
    # or overrides via environment variable for PostgreSQL in Docker/production.
    DATABASE_URL: str = "sqlite+aiosqlite:///./sentimentiq.db"

    # ML Inference configuration
    MODEL_TYPE: str = "champion"  # "champion" or "baseline"
    DEVICE: str = "cpu"

    # CORS configuration
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000",
        "*"
    ]

    RATE_LIMIT_PER_MINUTE: int = 120

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )


settings = Settings()

