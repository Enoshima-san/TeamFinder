from pydantic import Field
from pydantic.types import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseSettings(BaseSettings):
    driver: str
    host: str
    port: str
    name: str
    user: str
    password: SecretStr = Field(exclude=True)

    def get_dsn(self) -> str:
        """
        Возвращает строку подключения к БД со всеми секретами
        """
        return (
            f"{self.driver}://{self.user}:"
            f"{self.password.get_secret_value()}@"
            f"{self.host}:{self.port}/{self.name}"
        )

    def get_safe_dsn(self) -> str:
        """
        Возвращает строку подключения без критически важных `секретов`
        (идеально для логироавния)
        """
        return f"some_driver://{self.user}:******@main_db:{self.port}/{self.name}"

    model_config = SettingsConfigDict(
        env_prefix="DB_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )
