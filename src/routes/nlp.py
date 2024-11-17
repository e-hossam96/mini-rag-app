"""Implementation of NLP routes."""

from fastapi.responses import JSONResponse
from fastapi import APIRouter, status, Request
from schemes.nlp import PushRequest, SearchRequest
from models.enums.ResponseConfig import ResponseConfig
from models.ChunkDataModel import ChunkDataModel
from models.db_schemes.data_chunk import DataChunk

nlp_router = APIRouter(prefix="/api/v1/nlp", tags=["api_v1", "nlp"])


@nlp_router.post("/index/push/{project_id}")
async def index_project(
    request: Request, project_id: str, push_request: PushRequest
) -> JSONResponse:
    pass


@nlp_router.get("/index/info/{project_id}")
async def get_project_index_info(request: Request, project_id: str) -> JSONResponse:
    pass


@nlp_router.post("/index/push/{project_id}")
async def search_index(
    request: Request, project_id: str, search_request: SearchRequest
) -> JSONResponse:
    pass
