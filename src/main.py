"""Main FastAPI application."""

from fastapi import FastAPI
from routes import base, data
from helpers.config import get_settings, Settings
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from contextlib import asynccontextmanager


def connect_mongo(
    app_settinigs: Settings = get_settings(),
) -> tuple[AsyncIOMotorClient, AsyncIOMotorDatabase]:
    # get mongo connection and db client
    mongodb_connection = AsyncIOMotorClient(host=app_settinigs.MONGODB_URL)
    mongodb_db_client = mongodb_connection[app_settinigs.MONGODB_DATABASE]
    return mongodb_connection, mongodb_db_client


@asynccontextmanager
async def connect_mongo_lifespan(app: FastAPI):
    db_connection, db_client = connect_mongo()
    app.db_connection = db_connection
    app.db_client = db_client
    yield
    app.db_connection.close()


app = FastAPI(lifespan=connect_mongo_lifespan)


app.include_router(base.base_router)
app.include_router(data.data_router)
