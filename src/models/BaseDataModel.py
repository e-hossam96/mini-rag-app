"""Defining Base Data Model class."""

from helpers.config import get_settings
from motor.motor_asyncio import AsyncIOMotorClient


class BaseDataModel:
    def __init__(self, db_client: AsyncIOMotorClient) -> None:
        self.db_client = db_client
        self.app_settings = get_settings()
