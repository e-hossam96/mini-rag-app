"""Implementation of Vector DB Controller class."""

import pathlib
from .BaseController import BaseController
from fastapi import FastAPI
from helpers.config import Settings
from models.db_schemes.VectorDBDoc import VectorDBDoc
from models.ChunkDataModel import ChunkDataModel
from models.ProjectDataModel import ProjectDataModel


class VectorDBController(BaseController):
    def __init__(self, app: FastAPI, app_settings: Settings) -> None:
        super().__init__()
        self.db_client = app.db_client
        self.embedding_client = app.embedding_client
        self.vectordb_client = app.vectordb_client

    def get_vectordb_path(self, vectordb_name: str) -> pathlib.Path:
        vectordb_path = self.vectordb_dir_path.joinpath(vectordb_name)
        # take care when using parents in mkdir
        # we are sure parents exist. we will set it to True
        # in case project has nested directories
        vectordb_path.mkdir(parents=True, exist_ok=True)
        return vectordb_path

    def get_collection_name(self, project_id: str) -> str:
        return f"collection_{project_id}".strip()
