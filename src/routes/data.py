"""Implementaation of data routers."""

from controllers.DataController import DataController
from fastapi import APIRouter, Depends, UploadFile
from helpers.config import get_settings, Settings

data_router = APIRouter(prefix="/api/v1/data", tags=["api_v1", "data"])


@data_router.post("/upload/{project_id}")
async def upload_data(
    project_id: str, file: UploadFile, app_settings: Settings = Depends(get_settings)
) -> dict:
    # validate file settings
    is_valid, signal = DataController().validate_upload_file(file)
    resp = {"status": is_valid, "signal": signal}
    return resp
