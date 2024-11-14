"""Implementing Qdrant Vector DB Provider class"""

import pathlib
import logging
from typing import Union, Optional
from qdrant_client import QdrantClient, models
from ..VectorDBConfig import DistanceMethodConfig
from ..VectorDBInterface import VectorDBInterface


class QdrantDBProvider(VectorDBInterface):
    def __init__(self, db_path: pathlib.Path, distance_method: str) -> None:
        self.client = None
        self.db_path = db_path
        # define distance metric
        # only support cosine and dot
        if distance_method == DistanceMethodConfig.COSINE.value:
            self.distance_method = models.Distance.COSINE
        elif distance_method == DistanceMethodConfig.DOT.value:
            self.distance_method = models.Distance.DOT
        self.logger = logging.getLogger(__file__)

    def connect(self) -> bool:
        self.client = QdrantClient(path=str(self.db_path))
        return self.client is not None

    def disconnect(self) -> bool:
        self.client = None
        return self.client is None

    def is_collection(self, collection_name: str) -> bool:
        return self.client.collection_exists(collection_name=collection_name)

    def list_all_collections(self) -> list:
        return self.client.get_collections()

    def get_collection_info(self, collection_name: str) -> Union[dict, None]:
        collection_info = None
        if self.is_collection(collection_name):
            collection_info = self.client.get_collection(
                collection_name=collection_name
            )
        return collection_info

    def delete_collection(self, collection_name: str) -> bool:
        # I assume this method does the validation internally
        return self.client.delete_collection(collection_name=collection_name)

    def create_collection(
        self, collection_name: str, embedding_size: int, do_reset: bool = False
    ) -> bool:
        result = False
        if do_reset:
            _ = self.delete_collection(collection_name)
        if not self.is_collection(collection_name):
            result = self.client.create_collection(
                collection_name=collection_name,
                vectors_config=models.VectorParams(
                    size=embedding_size, distance=self.distance_method
                ),
            )
        return result

    def insert_one(
        self,
        collection_name: str,
        vector: list[float],
        metadata: dict,
        record_id: Optional[str] = None,
    ) -> bool:
        result = False
        if self.is_collection(collection_name):
            # metadata is a dict that has the text and other values
            self.client.upsert(
                collection_name=collection_name,
                points=[
                    models.PointStruct(vector=vector, payload=models.Payload(metadata))
                ],
            )
            result = True
        return result

    def inset_many(
        self,
        collection_name: str,
        vectors: list[list[float]],
        metadata: list[dict],
        record_ids: Optional[list[str]] = None,
        batch_size: int = 64,
    ) -> bool:
        result = False
        if self.is_collection(collection_name):
            self.client.upload_collection(
                collection_name=collection_name,
                vectors=vectors,
                payload=[models.Payload(m) for m in metadata],
                batch_size=batch_size,
            )

    def search_by_vector(
        self, collection_name: str, vector: list[float], limit: int = 10
    ):
        result = None
        if self.is_collection(collection_name):
            result = self.client.search(
                collection_name=collection_name,
                query_vector=vector,
                limit=limit,
            )
        return result
