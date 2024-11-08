"""Implementaation of data routers."""

from controllers.DataController import DataController
from controllers.ProcessController import ProcessController
from fastapi import APIRouter, UploadFile, status, Request
from fastapi.responses import JSONResponse
from .schemes.data import ProcessRequest
from models.enums.ResponseSignal import ResponseSignal
from typing import Union
from langchain_core.documents.base import Document
from models.ProjectModel import ProjectModel
from models.ChunkModel import ChunkModel
from models.db_schemes.data_chunk import DataChunk

data_router = APIRouter(prefix="/api/v1/data", tags=["api_v1", "data"])


@data_router.post("/upload/{project_id}")
async def upload_data(
    request: Request,
    project_id: str,
    file: UploadFile,
) -> JSONResponse:
    data_controller = DataController()
    # validate file settings
    is_valid, validation_signal = data_controller.validate_upload_file(file)
    if not is_valid:
        resp = JSONResponse(
            content={"signal": validation_signal},
            status_code=status.HTTP_400_BAD_REQUEST,
        )
        return resp
    # upload file to server
    project_model = await ProjectModel.create_instance(request.app.db_client)
    project = await project_model.get_project(project_id=project_id)
    file_path, file_id = data_controller.get_unique_file_path(project_id, file.filename)
    is_written, write_signal = await data_controller.write_uploaded_file(
        file, file_path
    )
    resp_content = {"signal": write_signal}
    if is_written:
        resp_content["file_id"] = file_id
        resp_content["project_id"] = str(project._id)
        resp = JSONResponse(content=resp_content, status_code=status.HTTP_200_OK)
    else:
        resp = JSONResponse(
            content=resp_content, status_code=status.HTTP_400_BAD_REQUEST
        )
    return resp


@data_router.post("/process/{project_id}")
async def process_data(
    request: Request, project_id: str, process_request: ProcessRequest
) -> JSONResponse:
    process_file_id = process_request.process_file_id
    process_chunk_size = process_request.process_chunk_size
    process_overlap_size = process_request.process_overlap_size
    process_do_reset = process_request.process_do_reset
    process_controller = ProcessController(project_id)
    file_content = process_controller.get_file_content(process_file_id)
    if file_content is None:
        return JSONResponse(
            content={"signal": ResponseSignal.FILE_PROCESS_FAILED.value},
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    chunks = process_controller.process_file_content(
        file_content, process_chunk_size, process_overlap_size
    )
    # get project _id from db
    project_model = await ProjectModel.create_instance(request.app.db_client)
    project = await project_model.get_project(project_id=project_id)
    # create data chunk objects
    data_chunks = [
        DataChunk(
            chunk_text=chunk.page_content,
            chunk_metadata=chunk.metadata,
            chunk_index=i,
            chunk_project_id=project._id,
        )
        for i, chunk in enumerate(chunks)
    ]
    # write chunks to db using chunk model object
    chunk_model = await ChunkModel.create_instance(request.app.db_client)
    if process_do_reset:
        _ = await chunk_model.clear_project_chunks(project._id)  # id in db
    num_inserted_chunks = await chunk_model.batch_insert_chunks(data_chunks)
    return JSONResponse(
        content={
            "signal": ResponseSignal.FILE_PROCESS_SUCCEEDED.value,
            "num_chunks": num_inserted_chunks,
        },
        status_code=status.HTTP_200_OK,
    )
