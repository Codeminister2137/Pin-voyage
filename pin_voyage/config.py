from typing import Any

from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str

    DATABASE_URL: str | None = None
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="allow", env_ignore_empty=True
    )

    def model_post_init(self, context: Any, /) -> None:
        self.DATABASE_URL = f"postgresql+psycopg2://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"


def get_config() -> Config:
    """Logic returning relevant config - to be developed"""
    return Config()


settings = get_config()
