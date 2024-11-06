"""Implementing project schema for mongo database."""

from pydantic import BaseModel, Field, field_validator
from bson.objectid import ObjectId
from typing import Optional


class Project(BaseModel):
    _id: Optional[ObjectId]
    project_id: str = Field(min_length=1)

    @field_validator("project_id")
    @classmethod
    def validate_project_id(cls, value: str) -> str:
        if not value.isalnum():
            raise ValueError("{project_id} must be Alpha Numeric")
        return value

    class config:
        arbitrary_types_allowed = True
