"""Defining base configurations variables."""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APPLICATION_NAME: str
    APPLICATION_VERSION: str

    FILE_ALLOWED_TYPES: list[str]
    FILE_MAX_SIZE: int
    FILE_CHUNK_SIZE: int

    MONGODB_URL: str
    MONGODB_DATABASE: str

    GENERATION_BACKEND: str
    EMBEDDING_BACKEND: str

    OPENAI_API_KEY: str = None
    OPENAI_BASE_URL: str = None

    COHERE_API_KEY: str = None
    COHERE_BASE_URL: str = None

    GENERATION_MODEL_ID: str = None

    EMBEDDING_MODEL_ID: str = None
    EMBEDDING_MODEL_SIZE: int = None

    MAX_INPUT_CHARACTERS: int = None
    MAX_OUTPUT_TOKENS: int = None
    TEMPERATURE: float = None

    VECTORDB_BACKEND: str
    VECTORDB_DISTANCE: str = None

    class Config:
        env_file = ".env"


def get_settings() -> Settings:
    return Settings()
