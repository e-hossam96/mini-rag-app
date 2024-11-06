"""Implementing data chunk schema for mongo database."""

from pydantic import BaseModel, Field
from bson.objectid import ObjectId
from typing import Optional


class DataChunk(BaseModel):
    _id: Optional[ObjectId]
    chunk_text: str = Field(min_length=1)
    chunk_metadata: dict
    chunk_index: int = Field(ge=0)
    chunk_project_id: ObjectId

    class config:
        arbitrary_types_allowed = True
