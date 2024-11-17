"""Implementation of NLP routes."""

from fastapi.responses import JSONResponse
from fastapi import APIRouter, status, Request
from .schemes.nlp import PushRequest, SearchRequest
from models.enums.ResponseConfig import ResponseConfig
from models.ChunkDataModel import ChunkDataModel
from models.db_schemes.data_chunk import DataChunk
from models.ProjectDataModel import ProjectDataModel
from stores.llm.LLMConfig import DocTypeConfig
from helpers.config import get_settings

nlp_router = APIRouter(prefix="/api/v1/nlp", tags=["api_v1", "nlp"])


@nlp_router.post("/index/push/{project_id}")
async def index_project(
    request: Request, project_id: str, push_request: PushRequest
) -> JSONResponse:
    project_model = await ProjectDataModel.create_instance(request.app.db_client)
    chunk_model = await ChunkDataModel.create_instance(request.app.db_client)
    project = await project_model.get_project(project_id=project_id)
    # get chunks using project id
    chunks_batch, num_pages = await chunk_model.get_all_project_chunks(project._id)
    project_chunks = [] + chunks_batch
    for page_index in range(1, num_pages):
        chunks_batch, _ = await chunk_model.get_all_project_chunks(
            project._id, page_index
        )
        project_chunks.extend(chunks_batch)
    if not project_chunks:
        return JSONResponse(
            content={"signal": ResponseConfig.NO_CHUNKS_ERROR.value},
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    # embed all the texts of the chunks
    vectors = [
        request.app.embedding_client.embed_text(
            chunk.chunk_text, DocTypeConfig.DOC.value
        )
        for chunk in project_chunks
    ]
    if not vectors or None in vectors:
        return JSONResponse(
            content={"signal": ResponseConfig.EMBEDDING_CHUNKS_FAILED.value},
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    # inset vectors into vector db
    app_settings = get_settings()
    collection_name = f"collection_{project_id}"
    _ = request.app.vectordb_client.create_collection(
        collection_name=collection_name,
        embedding_size=app_settings.EMBEDDING_MODEL_SIZE,
        do_reset=push_request.do_reset,
    )
    meta_data = [chunk.chunk_metadata for chunk in project_chunks]
    texts = [chunk.chunk_text for chunk in project_chunks]
    for md, t in zip(meta_data, texts):
        md["text"] = t
    result = request.app.vectordb_client.insert_many(
        collection_name=collection_name,
        vectors=vectors,
        metadata=meta_data,
    )
    if result:
        return JSONResponse(
            content={"signal": ResponseConfig.VECTORDB_INDEXING_SUCCEEDED.value},
            status_code=status.HTTP_200_OK,
        )
    else:
        return JSONResponse(
            content={"signal": ResponseConfig.VECTORDB_INDEXING_FALIED.value},
            status_code=status.HTTP_400_BAD_REQUEST,
        )


@nlp_router.get("/index/info/{project_id}")
async def get_project_index_info(request: Request, project_id: str) -> JSONResponse:
    pass


@nlp_router.post("/index/push/{project_id}")
async def search_index(
    request: Request, project_id: str, search_request: SearchRequest
) -> JSONResponse:
    pass
