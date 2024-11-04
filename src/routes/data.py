"""Implementaation of data routers."""

from controllers.DataController import DataController
from controllers.ProjectController import ProjectController
from fastapi import APIRouter, Depends, UploadFile, status
from fastapi.responses import JSONResponse
from helpers.config import get_settings, Settings

data_router = APIRouter(prefix="/api/v1/data", tags=["api_v1", "data"])


@data_router.post("/upload/{project_id}")
async def upload_data(
    project_id: str, file: UploadFile, app_settings: Settings = Depends(get_settings)
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
    project_path = ProjectController().get_project_path(project_id)
    file_path = project_path.joinpath(file.filename)
    is_written, write_signal = await data_controller.write_uploaded_file(file, file_path)
    resp_content = {"signal": write_signal}
    if is_written:
        resp = JSONResponse(content=resp_content, status_code=status.HTTP_200_OK)
    else:
        resp = JSONResponse(
            content=resp_content, status_code=status.HTTP_400_BAD_REQUEST
        )
    return resp
