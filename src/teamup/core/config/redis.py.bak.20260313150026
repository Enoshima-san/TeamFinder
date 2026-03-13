from pydantic_settings import BaseSettings, SettingsConfigDict


class RedisSettings(BaseSettings):
    host: str
    port: str
    db: int

    def get_dsn(self) -> str:
        return f"{self.host}://{self.port}/{self.db}"

    model_config = SettingsConfigDict(
        env_prefix="REDIS_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )
