"""Implementation of Vector DB Controller class."""

import pathlib
from .BaseController import BaseController
from fastapi import FastAPI
from helpers.config import Settings
from models.db_schemes.VectorDBDoc import VectorDBDoc
from models.db_schemes.DataChunk import DataChunk
from stores.llm.LLMConfig import DocTypeConfig


class VectorDBController(BaseController):
    def __init__(self) -> None:
        super().__init__()

    def get_vectordb_path(self, vectordb_name: str) -> pathlib.Path:
        vectordb_path = self.vectordb_dir_path.joinpath(vectordb_name)
        # take care when using parents in mkdir
        # we are sure parents exist. we will set it to True
        # in case project has nested directories
        vectordb_path.mkdir(parents=True, exist_ok=True)
        return vectordb_path

    def get_collection_name(self, project_id: str) -> str:
        return f"collection_{project_id}".strip()

    def index_into_vectordb(
        self,
        app: FastAPI,
        app_settings: Settings,
        chunks: list[DataChunk],
        collection_name: str,
        do_reset: bool,
    ) -> bool:
        result = False
        # get needed data for embedding from DataChunk objects
        vectors = [
            app.embedding_client.embed_text(chunk.chunk_text, DocTypeConfig.DOC.value)
            for chunk in chunks
        ]
        if vectors is None or len(vectors) == 0:
            return result
        # inset vectors into vector db
        _ = app.vectordb_client.create_collection(
            collection_name=collection_name,
            embedding_size=app_settings.EMBEDDING_MODEL_SIZE,
            do_reset=do_reset,
        )
        meta_data = [chunk.chunk_metadata for chunk in chunks]
        texts = [chunk.chunk_text for chunk in chunks]
        for md, t in zip(meta_data, texts):
            md["text"] = t
        result = app.vectordb_client.insert_many(
            collection_name=collection_name,
            vectors=vectors,
            metadata=meta_data,
        )
        return result
