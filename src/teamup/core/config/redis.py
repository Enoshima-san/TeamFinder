```python
from pydantic import BaseSettings, SettingsConfigDict

class RedisSettings(BaseSettings):
    """
    Settings for Redis connection.

    Attributes:
        host (str): Redis host.
        port (str): Redis port.
        db (int): Redis database number.
    """

    host: str = ...  # Redis host
    port: str = ...  # Redis port
    db: int = ...  # Redis database number

    def get_dsn(self) -> str:
        """
        Returns the Redis DSN (Data Source Name).

        Returns:
            str: Redis DSN.
        """
        return f"{self.host}://{self.port}/{self.db}"

    class Config(SettingsConfigDict):
        """
        Configuration for Redis settings.

        Attributes:
            env_prefix (str): Environment variable prefix.
            env_file (str): Path to environment file.
            env_file_encoding (str): Encoding for environment file.
            extra (str): Behavior for extra configuration.
        """
        env_prefix = "REDIS_"
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"
```