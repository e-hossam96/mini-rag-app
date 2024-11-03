"""Defining base configurations variables."""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APPLICATION_NAME: str
    APPLICATION_VERSION: str
    FILE_ALLOWED_TYPES: list[str]
    FILE_MAX_SIZE: int

    class Config:
        env_file = ".env"


def get_settings() -> Settings:
    return Settings()
