"""Defining Asset Model class and its methods."""

from .BaseDataModel import BaseDataModel
from motor.motor_asyncio import AsyncIOMotorDatabase
from .enums.DatabaseConfig import DatabaseConfig
from .db_schemes.asset import Asset
from bson.objectid import ObjectId


class AssetModel(BaseDataModel):
    def __init__(self, db_client: AsyncIOMotorDatabase) -> None:
        super().__init__(db_client)
        self.collection_name = DatabaseConfig.ASSET_COLLECTION_NAME.value
        self.db_collection = self.db_client[self.collection_name]

    async def init_collection(self) -> None:
        collection_names = await self.db_client.list_collection_names()
        if self.collection_name not in collection_names:
            indexes = Asset.get_indexes()
            for index in indexes:
                await self.db_collection.create_index(**index)

    @classmethod
    async def create_instance(
        cls, db_client: AsyncIOMotorDatabase
    ) -> AsyncIOMotorDatabase:
        instance = cls(db_client)
        await instance.init_collection()
        return instance

    async def create_asset(self, asset: Asset) -> Asset:
        asset_db_id = await self.db_collection.insert_one(asset.model_dump())
        asset._id = asset_db_id.inserted_id
        return asset

    async def get_all_project_assets(self, project_id: str) -> list[Asset]:
        records = await self.db_collection.find(
            {"asset_project_id": ObjectId(project_id)}
        ).to_list()
        assets = [Asset(**record) for record in records]
        return assets
