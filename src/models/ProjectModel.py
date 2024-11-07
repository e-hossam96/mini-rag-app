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

    async def get_project(self, project_id: str) -> Project:
        # get project by project_id
        # create new one if not existing
        project = Project(project_id)
        record = self.db_collection.find_one({"project_id": project_id})
        if record is None:
            project = await self.create_project(project)
        else:
            project._id = record._id
        return project

    async def get_all_project(
        self, page_index: int = 0, page_size: int = 10
    ) -> tuple[list[Project], int]:
        num_records = await self.db_collection.count_documents({})
        num_pages = num_records // page_size
        num_pages += 1 if num_records % page_size else 0
        cursor = self.db_collection.find().skip(page_index * page_size).limit(page_size)
        projects = []
        async for record in cursor:
            projects.append(Project(**record))
        return projects, num_pages
