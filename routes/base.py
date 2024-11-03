"""Implementaation of base routers."""

from fastapi import APIRouter


base_router = APIRouter()


@base_router.get("/")
def welcome() -> dict:
    resp = {"message": "Hello All!"}
    return resp
