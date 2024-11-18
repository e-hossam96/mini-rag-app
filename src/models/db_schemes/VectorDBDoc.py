"""Implementing document schema for vector database."""

from pydantic import BaseModel


class VectorDBDoc(BaseModel):
    text: str
    score: float
