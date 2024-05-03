"""Установка глобальных конфигов из файла .env."""
from __future__ import annotations

from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    """Загружаем глобальные конфиги переменных окружения"""

    version: str = Field(default="0.0.0")

    debug: bool = Field(default=False)
    log_level: str = Field(default="INFO")
    environment: str | None = Field(default=None)
    public_prefix: str = Field(default="/api/main/public")
    private_prefix: str = Field(default="/api/main/private")
    admin_prefix: str = Field(default="/api/main/service")

    postgres_host: str = Field(default="localhost")
    postgres_port: int = Field(default=5432)
    postgres_user: str = Field(default="postgres")
    postgres_password: str = Field(default="postgres")
    postgres_db: str = Field(default="template")
    postgres_db_schema: str | None = Field(default=None)

    project_name: str = Field(default="template")

    redis_host: str = Field(default="localhost")
    redis_port: int = Field(default=6379)

    redis_cache_time: int = Field(default=600)

    domain: str = Field(default="localhost")

    bot_token: str = Field(default="")
    chat_id: str = Field(default="")
    tg_domain: str = Field(default="https://api.telegram.org")

    secret_key: str = Field(default="")
    algorithm: str = Field(default="")

    @property
    def pg_db_creds(self) -> str:
        """Формируем строку с кредами"""
        return f"{self.postgres_user}:{self.postgres_password}"

    @property
    def db_url(self) -> str:
        """DSN c параметрами подключения к БД"""
        url = (
            f"postgresql+asyncpg://"
            f"{self.pg_db_creds}@"
            f"{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )

        return url

    @property
    def redis_cache_url(self) -> str:
        return f"redis://{self.redis_host}:{self.redis_port}/1"

    @property
    def tg_base_url(self) -> str:
        """Формируем строку с кредами"""
        return f"{self.tg_domain}/bot{self.bot_token}"

    class Config:
        """Путь к файлу .env."""

        env_file = ".env"


config = Settings()
