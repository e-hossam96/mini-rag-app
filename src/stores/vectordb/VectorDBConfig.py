"""Implementing the VectorDB Configuration enumeration class."""

from enum import Enum


class VectorDBConfig(Enum):
    QDRANT: str = "qdrant"


class DistanceMethodConfig(Enum):
    COSINE: str = "cosine"
    DOT: str = "dot"
