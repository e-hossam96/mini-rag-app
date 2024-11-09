"""Implementaation of data routers."""

import logging
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
from models.AssetModel import AssetModel
from models.db_schemes.data_chunk import DataChunk
from models.db_schemes.asset import Asset
from models.enums.AssetConfig import AssetConfig

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
    # store asset into database
    asset_model = await AssetModel.create_instance(request.app.db_client)
    asset = Asset(
        asset_project_id=project._id,
        asset_type=AssetConfig.FILE_TYPE_NAME.value,
        asset_name=file_id,
        asset_size=file_path.stat().st_size,
    )
    asset = await asset_model.create_asset(asset)
    resp_content = {"signal": write_signal}
    if is_written:
        resp_content["file_id"] = str(asset._id)
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

    # define all needed models
    project_model = await ProjectModel.create_instance(request.app.db_client)
    project = await project_model.get_project(project_id=project_id)
    chunk_model = await ChunkModel.create_instance(request.app.db_client)
    asset_model = await AssetModel.create_instance(request.app.db_client)

    # get file ids/names
    process_file_ids = []
    if process_file_id is None:
        # get all project asset file ids/names (files only now)
        project_assets = await asset_model.get_all_project_assets(
            project._id, AssetConfig.FILE_TYPE_NAME.value
        )
        asset_ids = [asset.asset_name for asset in project_assets]
        process_file_ids.extend(asset_ids)
    else:
        process_file_ids.append(process_file_id)

    if not process_file_ids:
        return JSONResponse(
            content={"signal": ResponseSignal.NO_FILES_ERROR.value},
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    if process_do_reset:
        _ = await chunk_model.clear_project_chunks(project._id)  # id in db

    num_chunks = 0
    num_files = 0
    # loop over all file ids/names and process them
    for process_file_id in process_file_ids:
        logging.info(f"Processing file: {process_file_id}")
        file_content = process_controller.get_file_content(process_file_id)
        if file_content is None:
            # return JSONResponse(
            #     content={"signal": ResponseSignal.FILE_PROCESS_FAILED.value},
            #     status_code=status.HTTP_400_BAD_REQUEST,
            # )
            logging.error(f"File missing or empty content for file: {process_file_id}")
            continue
        chunks = process_controller.process_file_content(
            file_content, process_chunk_size, process_overlap_size
        )
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
        num_chunks += await chunk_model.batch_insert_chunks(data_chunks)
        num_files += 1

    return JSONResponse(
        content={
            "signal": ResponseSignal.FILE_PROCESS_SUCCEEDED.value,
            "num_chunks": num_chunks,
            "num_files": num_files,
        },
        status_code=status.HTTP_200_OK,
    )
