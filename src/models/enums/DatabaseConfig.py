"""Defining Database configurations."""

from enum import Enum


class DatabaseConfig(Enum):
    PROJECT_COLLECTION_NAME: str = "projects"
    CHUNK_COLLECTION_NAME: str = "chunks"
    ASSET_COLLECTION_NAME: str = "assets"
