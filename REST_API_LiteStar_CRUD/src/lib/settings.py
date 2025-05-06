from __future__ import annotations

import os
from typing import Literal

from litestar.config.allowed_hosts import AllowedHostsConfig
from litestar.config.cors import CORSConfig
from litestar.config.csrf import CSRFConfig
from litestar.logging import LoggingConfig
from litestar.openapi.config import OpenAPIConfig
from litestar.openapi.controller import OpenAPIController
from litestar.types import Method

from advanced_alchemy.base import orm_registry

from pydantic import BaseSettings, SecretStr, PostgresDsn


class Settings(BaseSettings):
    """Application settings."""

    class Config:
        env_file = ".env"
        case_sensitive = True

    DEBUG: bool = False
    SECRET_KEY: SecretStr = SecretStr("super-secret-key")

    # Database
    DATABASE_URL: PostgresDsn = "postgresql+asyncpg://postgres:postgres@localhost:5432/postgres"
    ECHO_SQL: bool = False

    # OpenAPI
    OPENAPI_PATH: str = "/api/docs"


settings = Settings()


def get_settings() -> Settings:
    """Get the application settings."""
    return settings


def config_cors() -> CORSConfig:
    """Configure CORS."""
    return CORSConfig(
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
        allow_credentials=True,
    )


def config_csrf() -> CSRFConfig:
    """Configure CSRF."""
    return CSRFConfig(
        secret=settings.SECRET_KEY.get_secret_value(),
        safe_methods={"GET", "OPTIONS"},
    )


def config_allowed_hosts() -> AllowedHostsConfig:
    """Configure allowed hosts."""
    return AllowedHostsConfig(
        allowed_hosts=["*"],
    )


def config_openapi() -> OpenAPIConfig:
    """Configure OpenAPI."""
    return OpenAPIConfig(
        title="User API",
        description="REST API for user management",
        version="1.0.0",
        path=settings.OPENAPI_PATH,
        root_schema_site="swagger",
        openapi_controller=OpenAPIController,
    )


def config_logging() -> LoggingConfig:
    """Configure logging."""
    return LoggingConfig(
        root={"level": "INFO", "handlers": ["console"]},
        loggers={
            "app": {"level": "INFO", "handlers": ["console"], "propagate": False},
            "uvicorn.access": {
                "level": "WARNING",
                "handlers": ["console"],
                "propagate": False,
            },
            "uvicorn.error": {
                "level": "INFO",
                "handlers": ["console"],
                "propagate": False,
            },
            "sqlalchemy.engine": {
                "level": "WARNING",
                "handlers": ["console"],
                "propagate": False,
            },
        },
    )
