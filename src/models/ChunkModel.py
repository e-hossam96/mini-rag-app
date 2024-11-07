"""Defining Chunk Model class and its methods."""

from .BaseDataModel import BaseDataModel
from motor.motor_asyncio import AsyncIOMotorDatabase
from .enums.DatabaseConfig import DatabaseConfig
from .db_schemes.data_chunk import DataChunk
from typing import Union
from bson.objectid import ObjectId
from pymongo import InsertOne


class ChunkModel(BaseDataModel):
    def __init__(self, db_client: AsyncIOMotorDatabase) -> None:
        super().__init__(db_client)
        self.db_collection = self.db_client[DatabaseConfig.CHUNK_COLLECTION_NAME.value]

    async def create_chunk(self, chunk: DataChunk) -> DataChunk:
        chunk_db_id = await self.db_collection.insert_one(chunk.model_dump())
        chunk._id = chunk_db_id.inserted_id
        return chunk

    async def get_chunk(self, chunk_id: str) -> Union[DataChunk, None]:
        record = await self.db_collection.find_one({"_id": ObjectId(chunk_id)})
        if record is None:
            return None
        return DataChunk(**record)

    async def batch_insert_chunks(
        self, chunks: list[DataChunk], batch_size: int = 64
    ) -> int:
        num_chunks = len(chunks)
        # implement batch operations
        for i in range(0, num_chunks, batch_size):
            batch_chunks = chunks[i : i + batch_size]
            # create operations
            batch_operations = [InsertOne(chunk.model_dump()) for chunk in batch_chunks]
            await self.db_collection.bulk_write(batch_operations)
        return num_chunks
