"""Implementing asset schema for mongo database."""

from pydantic import BaseModel, Field
from bson.objectid import ObjectId
from typing import Optional
import datetime


class Asset(BaseModel):
    _id: Optional[ObjectId]
    asset_project_id: ObjectId
    asset_name: str = Field(min_length=1)
    asset_type: str = Field(min_length=1)
    asset_size: int = Field(ge=0, default=None)  # size in bytes
    asset_pushed_at: datetime.datetime = Field(
        default=datetime.datetime.now(datetime.timezone.utc)
    )
    asset_config: Optional[dict] = Field(default=None)

    @classmethod
    def get_indexes(cls) -> list[dict]:
        indexes = [
            {
                "keys": [("asset_project_id", 1)],
                "name": "asset_project_id_index_1",
                "unique": False,
            },
            {
                "keys": [("asset_project_id", 1), ("asset_name", 1)],
                "name": "asset_project_id_name_index_1",
                "unique": True,
            },
        ]
        return indexes

    class Config:
        arbitrary_types_allowed = True
