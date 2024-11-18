"""Implementation of Vector DB Controller class."""

import json
import pathlib
from .BaseController import BaseController
from fastapi import FastAPI
from helpers.config import Settings
from models.db_schemes.DataChunk import DataChunk
from stores.llm.LLMConfig import DocTypeConfig
from typing import Union


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

    def get_vectordb_collection_info(
        self, app: FastAPI, collection_name: str
    ) -> Union[dict, None]:
        collection_info = app.vectordb_client.get_collection_info(
            collection_name=collection_name
        )
        if collection_info is not None:
            collection_info = json.loads(
                json.dumps(collection_info, default=lambda x: x.__dict__)
            )
        return collection_info

    def search_vectordb_collection(
        self, app: FastAPI, collection_name: str, text: str, limit: int
    ) -> Union[list[dict], None]:
        search_results = None
        query_vector = app.embedding_client.embed_text(
            text=text, doc_type=DocTypeConfig.DOC.value
        )
        if query_vector is None:
            return search_results
        search_results = app.vectordb_client.search_by_vector(
            collection_name=collection_name,
            vector=query_vector,
            limit=limit,
        )
        if search_results is not None:
            search_results = [
                record.model_dump(mode="json") for record in search_results
            ]
        return search_results

    def answer_rag_query(
        self, app: FastAPI, collection_name: str, text: str, limit: int
    ) -> Union[str, None]:
        ans = None
        search_results = self.search_vectordb_collection(
            app, collection_name, text, limit
        )
        if search_results is None:
            return ans
        # get prompt conponents
        system_msg = app.prompt_template.get_template(group="rag", key="system_prompt")
        augmentations = [
            app.prompt_template.get_template(
                group="rag",
                key="system_prompt",
                vars={"doc_num": i + 1, "chunk_text": doc["text"]},
            )
            for i, doc in enumerate(search_results)
        ]
        
