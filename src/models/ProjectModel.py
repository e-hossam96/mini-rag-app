"""Defining Project Model class and its methods."""

from .BaseDataModel import BaseDataModel
from motor.motor_asyncio import AsyncIOMotorDatabase
from .enums.DatabaseConfig import DatabaseConfig
from db_schemes.project import Project


class ProjectModel(BaseDataModel):
    def __init__(self, db_client: AsyncIOMotorDatabase) -> None:
        super().__init__(db_client)
        self.db_collection = self.db_client[
            DatabaseConfig.PROJECT_COLLECTION_NAME.value
        ]

    async def create_project(self, project: Project) -> Project:
        project_db_id = await self.db_collection.insert_one(**project.model_dump_json())
        project._id = project_db_id.inserted_id
        return project
