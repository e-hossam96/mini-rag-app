"""Main FastAPI application."""

from fastapi import FastAPI

app = FastAPI()


def welcome() -> dict:
    resp = {"message": "Hello World!"}
    return resp
