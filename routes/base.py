"""Implementaation of base routers."""

import os
from fastapi import APIRouter

base_router = APIRouter(prefix="/api/v1", tags=["api_v1"])


@base_router.get("/")
async def welcome() -> dict:
    resp = {
        "app_name": os.getenv("APPLICATION_NAME"),
        "app_version": os.getenv("APPLICATION_VERSION"),
    }
    return resp
