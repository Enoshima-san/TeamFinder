from pydantic_settings import BaseSettings, SettingsConfigDict


class ApplicationSettings(BaseSettings):
    name: str
    env: str
    debug: bool
    host: str
    port: int

    model_config = SettingsConfigDict(
        env_prefix="APP_",
        env_file=".env.example",
        env_file_encoding="utf-8",
        extra="ignore",
    )
