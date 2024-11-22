import logging
from enum import StrEnum
from pathlib import Path
from typing import Final
from urllib.parse import quote_plus

from pydantic import Field, RedisDsn
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.engine.url import URL


ROOT_DIR: Final[Path] = Path(__file__).parent.parent.parent.resolve()


class Environment(StrEnum):
    test = 'test'
    dev = 'dev'
    prod = 'prod'


class BaseEnvSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=ROOT_DIR / '.env',
        env_file_encoding='utf-8',
        case_sensitive=True,
        extra='ignore',
    )


class AppSettings(BaseEnvSettings):
    DEBUG: bool = False
    ENVIRONMENT: Environment = Environment.dev
    LOG_LEVEL: str = logging.getLevelName(logging.INFO)
    RAISE_ON_LOG_EXCEPTIONS: bool = False
    NAME: str = Field('stories-service', validation_alias='APPLICATION_NAME')


class DatabaseSettings(BaseEnvSettings):
    model_config = SettingsConfigDict(env_prefix='DB_')

    # Database
    HOST: str = 'postgres'
    PORT: int = 5432
    NAME: str = 'oss'
    USER: str = 'oss'
    PASSWORD: str = 'oss'

    # DB connection
    ECHO: bool = False

    # DB Pool
    POOL_MIN_SIZE: int = 1
    POOL_MAX_SIZE: int = 10
    POOL_TIMEOUT: int = 30
    POOL_PRE_PING: bool = False

    def dsn(self) -> URL:
        return URL.create(
            drivername='postgresql+asyncpg',
            username=self.USER,
            password=quote_plus(self.PASSWORD),
            host=self.HOST,
            port=self.PORT,
            database=self.NAME,
        )


class RedisSettings(BaseEnvSettings):
    """Redis settings for the application.

    Prefix all environment variables with `REDIS_`, e.g., `REDIS_URL`.
    """

    model_config = SettingsConfigDict(env_prefix='REDIS_')

    HOST: RedisDsn = 'redis://redis:6379/0'  # type: ignore[assignment]


class SentrySettings(BaseEnvSettings):
    """Configures sentry for the application."""

    model_config = SettingsConfigDict(env_prefix='SENTRY_')

    ENABLED: bool = Field(False, validation_alias='SENTRY_MODE')
    DSN: str | None = None
    TRACES_SAMPLE_RATE: float = 0.1
    STAGE_NAME: str = 'production'


class ServerSettings(BaseEnvSettings):
    """ASGI web server configuration."""

    model_config = SettingsConfigDict(env_prefix='UVICORN_')

    HOST: str = '0.0.0.0'  # noqa: S104
    LOG_LEVEL: str = logging.getLevelName(logging.INFO)
    PORT: int = 8000
    RELOAD: bool = True
    KEEPALIVE: int = 65


class OpenAPISettings(BaseEnvSettings):
    """Configures OpenAPI for the application.

    Prefix all environment variables with `OPENAPI_`, e.g., `OPENAPI_TITLE`.
    """

    model_config = SettingsConfigDict(env_prefix='OPENAPI_')

    TITLE: str = 'stories-service'
    DESCRIPTION: str | None = 'OSS OpenAPI schema'
    VERSION: str = '0.1.0'
    CONTACT_NAME: str = 'GS-Labs'


class TaskSettings(BaseEnvSettings):
    model_config = SettingsConfigDict(env_prefix='TASK_')

    REDIS_HOST: RedisDsn = 'redis://redis:6379/1'  # type: ignore[assignment]
    WORKER_NAME: str = 'background-worker'
    # Schedules
    REFRESH_STORY_SCHEDULE: str = '0 0 * * *'
    # Timeouts
    RUNTIME_TIMEOUT_SECONDS: int = 300


class StorySettings(BaseEnvSettings):
    model_config = SettingsConfigDict(env_prefix='STORY_')


app = AppSettings()
database = DatabaseSettings()
redis = RedisSettings()
sentry = SentrySettings()
server = ServerSettings()
openapi = OpenAPISettings()
task = TaskSettings()
story = StorySettings()
