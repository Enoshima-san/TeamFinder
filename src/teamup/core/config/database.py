```python
from pydantic import Field
from pydantic.types import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseSettings(BaseSettings):
    """
    Database connection settings.

    Attributes:
        driver (str): Database driver.
        host (str): Database host.
        port (str): Database port.
        name (str): Database name.
        user (str): Database username.
        password (SecretStr): Database password (hidden for security).
    """

    driver: str = Field(..., env="DB_DRIVER")
    host: str = Field(..., env="DB_HOST")
    port: str = Field(..., env="DB_PORT")
    name: str = Field(..., env="DB_NAME")
    user: str = Field(..., env="DB_USER")
    password: SecretStr = Field(..., env="DB_PASSWORD", exclude=True)

    def get_dsn(self) -> str:
        """
        Returns a database connection string with all secrets.

        Returns:
            str: Database connection string.
        """
        return (
            f"{self.driver}://{self.user}:{self.password.get_secret_value()}@"
            f"{self.host}:{self.port}/{self.name}"
        )

    def get_safe_dsn(self) -> str:
        """
        Returns a database connection string without critical secrets.

        This is ideal for logging purposes.

        Returns:
            str: Database connection string without secrets.
        """
        return f"some_driver://{self.user}:******@main_db:{self.port}/{self.name}"

    model_config = SettingsConfigDict(
        env_prefix="DB_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )
```