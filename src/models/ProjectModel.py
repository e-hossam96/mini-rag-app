"""Defining Project Model class and its methods."""

from .BaseDataModel import BaseDataModel
from motor.motor_asyncio import AsyncIOMotorDatabase
from .enums.DatabaseConfig import DatabaseConfig


class ProjectModel(BaseDataModel):
    def __init__(self, db_client: AsyncIOMotorDatabase) -> None:
        super().__init__(db_client)
        self.db_collection = self.db_client[
            DatabaseConfig.PROJECT_COLLECTION_NAME.value
        ]
