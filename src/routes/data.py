"""Implementaation of data routers."""

import aiofiles
from controllers.DataController import DataController
from controllers.ProjectController import ProjectController
from models.enums.ResponseSignal import ResponseSignal
from fastapi import APIRouter, Depends, UploadFile, status
from fastapi.responses import JSONResponse
from helpers.config import get_settings, Settings

data_router = APIRouter(prefix="/api/v1/data", tags=["api_v1", "data"])


@data_router.post("/upload/{project_id}")
async def upload_data(
    project_id: str, file: UploadFile, app_settings: Settings = Depends(get_settings)
) -> JSONResponse:
    # validate file settings
    is_valid, validation_signal = DataController().validate_upload_file(file)
    resp_code = status.HTTP_200_OK if is_valid else status.HTTP_400_BAD_REQUEST
    if not is_valid:
        resp_content = {"signal": validation_signal}
        resp = JSONResponse(content=resp_content, status_code=resp_code)
        return resp
    # upload file to server
    project_path = ProjectController().get_project_path(project_id)
    file_path = project_path.joinpath(file.filename)
    async with aiofiles.open(file_path, "wb") as f:
        while chunk := await file.read(
            size=app_settings.FILE_CHUNK_SIZE * 1_048_576
        ):  # walrus operator
            await f.write(chunk)
    resp_content = {"signal": ResponseSignal.FILE_UPLOAD_SUCCEEDED.value}
    resp = JSONResponse(content=resp_content, status_code=resp_code)
    return resp
