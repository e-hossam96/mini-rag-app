"""Main FastAPI application."""

from fastapi import FastAPI
from routes import base, data
from helpers.config import get_settings, Settings
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from contextlib import asynccontextmanager
from stores.llm.LLMProviderFactory import LLMProviderFactory
from stores.llm.providers.CoHereProvider import CoHereProvider
from stores.llm.providers.OpenAIProvider import OpenAIProvider


def connect_mongo(
    app_settinigs: Settings = get_settings(),
) -> tuple[AsyncIOMotorClient, AsyncIOMotorDatabase]:
    # get mongo connection and db client
    mongodb_connection = AsyncIOMotorClient(host=app_settinigs.MONGODB_URL)
    mongodb_db_client = mongodb_connection[app_settinigs.MONGODB_DATABASE]
    return mongodb_connection, mongodb_db_client


def connect_llm_providers(
    app: FastAPI, app_settinigs: Settings = get_settings()
) -> FastAPI:
    llm_provider_factory = LLMProviderFactory(app_settinigs)
    # setting generation and embedding clients
    app.generation_client = llm_provider_factory.create_provider(
        app_settinigs.GENERATION_BACKEND
    )
    app.embedding_client = llm_provider_factory.create_provider(
        app_settinigs.EMBEDDING_BACKEND
    )
    # setting api keys
    app.generation_client.set_generation_model(app_settinigs.GENERATION_MODEL_ID)
    app.embedding_client.set_embedding_model(
        app_settinigs.EMBEDDING_MODEL_ID, app_settinigs.EMBEDDING_MODEL_SIZE
    )
    return app


@asynccontextmanager
async def connect_mongo_lifespan(app: FastAPI):
    db_connection, db_client = connect_mongo()
    connect_llm_providers(app)
    app.db_connection = db_connection
    app.db_client = db_client
    yield
    app.db_connection.close()


app = FastAPI(lifespan=connect_mongo_lifespan)


app.include_router(base.base_router)
app.include_router(data.data_router)
