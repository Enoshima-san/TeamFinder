```python
from functools import lru_cache
from pydantic import Field
from pydantic_settings import BaseSettings

from .config.application import ApplicationSettings
from .config.database import DatabaseSettings
from .config.redis import RedisSettings
from .config.security import SecuritySettings


class BaseSettings(BaseSettings):
    """
    Base class for application settings, encapsulating sensitive information.
    """

    db: DatabaseSettings = Field(default_factory=DatabaseSettings)
    redis: RedisSettings = Field(default_factory=RedisSettings)
    application: ApplicationSettings = Field(default_factory=ApplicationSettings)
    security: SecuritySettings = Field(default_factory=SecuritySettings)


@lru_cache()
def get_application_settings() -> BaseSettings:
    """
    Returns the application settings instance, cached for performance.

    Returns:
        BaseSettings: The application settings instance.
    """
    return BaseSettings()


# Get the application settings instance
application_settings = get_application_settings()
```