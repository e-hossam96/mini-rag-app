"""Main FastAPI application."""

from fastapi import FastAPI
from routes import base, data
from helpers.config import get_settings, Settings
from motor.motor_asyncio import AsyncIOMotorClient
from contextlib import asynccontextmanager
from stores.llm.LLMProviderFactory import LLMProviderFactory


def connect_mongo(
    app: FastAPI,
    app_settinigs,
) -> FastAPI:
    # get mongo connection and db client
    app.db_connection = AsyncIOMotorClient(host=app_settinigs.MONGODB_URL)
    app.db_client = app.db_connection[app_settinigs.MONGODB_DATABASE]
    return app


def connect_llm_providers(app: FastAPI, app_settinigs: Settings) -> FastAPI:
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
    app_settinigs = get_settings()
    app = connect_mongo(app, app_settinigs)
    app = connect_llm_providers(app, app_settinigs)
    yield
    app.db_connection.close()


app = FastAPI(lifespan=connect_mongo_lifespan)


app.include_router(base.base_router)
app.include_router(data.data_router)
