"""Implementaation of base routers."""

from fastapi import APIRouter, Depends
from helpers.config import get_settings, Settings

base_router = APIRouter(prefix="/api/v1", tags=["api_v1"])


@base_router.get("/")
async def welcome(app_settings: Settings = Depends(get_settings)) -> dict:
    resp = {
        "app_name": app_settings.APPLICATION_NAME,
        "app_version": app_settings.APPLICATION_VERSION,
    }
    return resp
