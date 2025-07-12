from __future__ import annotations
import os
from pydantic_settings import BaseSettings
from pydantic import SecretStr

class Settings(BaseSettings):
    """Application settings."""
    
    class Config:
        env_file = ".env"
        case_sensitive = True

    DEBUG: bool = False
    SECRET_KEY: SecretStr = SecretStr("super-secret-key")
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@postgres:5432/users"
    ECHO_SQL: bool = False

settings = Settings()
