from functools import lru_cache
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Validated application configuration loaded from environment variables."""

    app_name: str = Field(default="FruitVision", alias="APP_NAME")
    app_env: Literal["development", "testing", "production"] = Field(
        default="development",
        alias="APP_ENV",
    )
    debug: bool = Field(default=False, alias="APP_DEBUG")

    database_url: str = Field(alias="DATABASE_URL")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )
    app_version: str = Field(default="0.1.0", alias="APP_VERSION")

    jwt_secret_key: str = Field(alias="JWT_SECRET_KEY")

    jwt_algorithm: str = "HS256"

    jwt_access_token_expire_minutes: int = 30


@lru_cache
def get_settings() -> Settings:
    """
    Return one cached Settings instance.

    Environment configuration does not need to be re-read every time another
    module asks for application settings.
    """
    return Settings()


settings = get_settings()
