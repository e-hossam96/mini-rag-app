"""Main FastAPI application."""

from fastapi import FastAPI

app = FastAPI()


@app.get("/welcome")
def welcome() -> dict:
    resp = {"message": "Hello World!"}
    return resp
