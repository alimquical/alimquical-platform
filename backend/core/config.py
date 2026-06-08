from pydantic_settings import BaseSettings
from typing import Optional, Union


class Settings(BaseSettings):
    APP_NAME: str = "Alimquical API"
    VERSION: str = "1.0.0"
    DEBUG: bool = False
    ENVIRONMENT: str = "production"

    DATABASE_URL: str
    DATABASE_POOL_SIZE: int = 20
    DATABASE_MAX_OVERFLOW: int = 10

    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    OPENAI_API_KEY: Optional[str] = None
    ANTHROPIC_API_KEY: Optional[str] = None
    GOOGLE_API_KEY: Optional[str] = None

    QDRANT_URL: Optional[str] = None
    QDRANT_API_KEY: Optional[str] = None

    REDIS_URL: Optional[str] = None
    CELERY_BROKER_URL: Optional[str] = None

    SENTRY_DSN: Optional[str] = None

    STORAGE_BUCKET: str = "alimquical"
    STORAGE_ENDPOINT: Optional[str] = None
    STORAGE_ACCESS_KEY: Optional[str] = None
    STORAGE_SECRET_KEY: Optional[str] = None

    WHITELIST_ORIGINS: list[str] = [
        "http://localhost:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:3001",
        "https://appmovilvercel.vercel.app",
        "https://frontend-dusky-chi-71.vercel.app",
        "https://frontend-jx0cloqbt-alimquicals-projects.vercel.app",
    ]

    WHATSAPP_API_TOKEN: Optional[str] = None
    WHATSAPP_PHONE_NUMBER_ID: Optional[str] = None

    model_config = {"env_file": ".env", "case_sensitive": True, "extra": "ignore"}

    @classmethod
    def _validate_bool(cls, v):
        if isinstance(v, bool):
            return v
        if isinstance(v, str):
            return v.strip().lower() in ("1", "true", "yes", "on")
        return False

    def get_database_url(self) -> str:
        return self.DATABASE_URL


settings = Settings()
