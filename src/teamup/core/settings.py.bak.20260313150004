from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings

from .config.application import ApplicationSettings
from .config.database import DatabaseSettings
from .config.redis import RedisSettings
from .config.security import SecuritySettings


class Settings(BaseSettings):
    """
    Базовый класс настроек, который отвечает инкапсулирование секретов
    """

    db: DatabaseSettings = Field(default_factory=DatabaseSettings)  # type: ignore[reportArgumentType]
    redis: RedisSettings = Field(default_factory=RedisSettings)  # type: ignore[reportArgumentType]
    application: ApplicationSettings = Field(default_factory=ApplicationSettings)  # type: ignore[reportArgumentType]
    security: SecuritySettings = Field(default_factory=SecuritySettings)  # type: ignore[reportArgumentType]


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
