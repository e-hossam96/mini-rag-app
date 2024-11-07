"""Defining Chunk Model class and its methods."""

from .BaseDataModel import BaseDataModel
from motor.motor_asyncio import AsyncIOMotorDatabase
from .enums.DatabaseConfig import DatabaseConfig
from .db_schemes.data_chunk import DataChunk


class ChunkModel(BaseDataModel):
    def __init__(self, db_client: AsyncIOMotorDatabase) -> None:
        super().__init__(db_client)
        self.db_collection = self.db_client[DatabaseConfig.CHUNK_COLLECTION_NAME.value]
