"""Implementaation of data routers."""

from controllers.DataController import DataController
from fastapi import APIRouter, Depends, UploadFile, status
from fastapi.responses import JSONResponse
from helpers.config import get_settings, Settings

data_router = APIRouter(prefix="/api/v1/data", tags=["api_v1", "data"])


@data_router.post("/upload/{project_id}")
async def upload_data(
    project_id: str, file: UploadFile, app_settings: Settings = Depends(get_settings)
) -> JSONResponse:
    # validate file settings
    is_valid, signal = DataController().validate_upload_file(file)
    resp_content = {"status": is_valid, "signal": signal}
    resp_code = status.HTTP_200_OK if is_valid else status.HTTP_400_BAD_REQUEST
    resp = JSONResponse(content=resp_content, status_code=resp_code)
    return resp
