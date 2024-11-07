"""Defining Project Model class and its methods."""

from .BaseDataModel import BaseDataModel
from motor.motor_asyncio import AsyncIOMotorClient


class ProjectModel(BaseDataModel):
    def __init__(self, db_client: AsyncIOMotorClient) -> None:
        super().__init__(db_client)
