"""Implementing the Vector DB Interface class."""

from typing import Union, Optional
from abc import ABC, abstractmethod
from models.db_schemes.VectorDBDoc import VectorDBDoc


class VectorDBInterface(ABC):
    @abstractmethod
    def connect(self) -> bool:
        pass

    @abstractmethod
    def disconnect(self) -> bool:
        pass

    @abstractmethod
    def is_collection(self, collection_name: str) -> bool:
        pass

    @abstractmethod
    def list_all_collections(self) -> list:
        pass

    @abstractmethod
    def get_collection_info(self, collection_name: str) -> Union[dict, None]:
        pass

    @abstractmethod
    def delete_collection(self, collection_name: str) -> bool:
        pass

    @abstractmethod
    def create_collection(
        self, collection_name: str, embedding_size: int, do_reset: bool = False
    ) -> bool:
        pass

    @abstractmethod
    def insert_one(
        self,
        collection_name: str,
        vector: list[float],
        metadata: dict,
        record_id: Optional[str] = None,
    ) -> bool:
        pass

    @abstractmethod
    def insert_many(
        self,
        collection_name: str,
        vectors: list[list[float]],
        metadata: list[dict],
        record_ids: Optional[list[str]] = None,
        batch_size: int = 64,
    ) -> bool:
        pass

    @abstractmethod
    def search_by_vector(
        self, collection_name: str, vector: list[float], limit: int = 10
    ) -> Union[list[VectorDBDoc], None]:
        pass
