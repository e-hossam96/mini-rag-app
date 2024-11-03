"""Implementaation of base routers."""

from fastapi import APIRouter


base_router = APIRouter(prefix="/app/v1", tags=["api_v1"])


@base_router.get("/")
def welcome() -> dict:
    resp = {"message": "Hello All!"}
    return resp
