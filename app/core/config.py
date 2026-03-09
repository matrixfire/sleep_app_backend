from __future__ import annotations

from typing import Any

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    APP_NAME: str = "sleep_app_backend"
    ENV: str = "dev"
    API_V1_STR: str = "/api/v1"

    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24

    MYSQL_HOST: str = "127.0.0.1"
    MYSQL_PORT: int = 3306
    MYSQL_USER: str = "root"
    MYSQL_PASSWORD: str = ""
    MYSQL_DB: str = "sleep_app"

    REDIS_HOST: str = "127.0.0.1"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_PASSWORD: str = ""

    CORS_ORIGINS: list[str] = []

    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        # mysql+pymysql://user:pass@host:port/db?charset=utf8mb4
        return (
            f"mysql+pymysql://{self.MYSQL_USER}:{self.MYSQL_PASSWORD}"
            f"@{self.MYSQL_HOST}:{self.MYSQL_PORT}/{self.MYSQL_DB}"
            f"?charset=utf8mb4"
        )

    def redis_kwargs(self) -> dict[str, Any]:
        kwargs: dict[str, Any] = {
            "host": self.REDIS_HOST,
            "port": self.REDIS_PORT,
            "db": self.REDIS_DB,
            "decode_responses": True,
        }
        if self.REDIS_PASSWORD:
            kwargs["password"] = self.REDIS_PASSWORD
        return kwargs


settings = Settings()

