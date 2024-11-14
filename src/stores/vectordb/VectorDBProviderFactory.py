"""Implementing the Vector DB Provider Factory class."""

from typing import Union
from .VectorDBConfig import VectorDBConfig
from .providers.QdrandDBProvider import QdrantDBProvider
from ...helpers.config import Settings
from ...controllers.VectorDBController import VectorDBController


class VectorDBProviderFactory:
    def __init__(self, app_settings: Settings) -> None:
        self.app_settings = app_settings
        self.vectordb_controller = VectorDBController()

    def create_provider(self, provider_name) -> Union[QdrantDBProvider, None]:
        provider = None
        provider_path = self.vectordb_controller.get_vectordb_path(provider_name)
        if self.app_settings.VECTORDB_BACKEND == VectorDBConfig.QDRANT.value:
            provider = QdrantDBProvider(
                db_path=provider_path,
                distance_method=self.app_settings.VECTORDB_DISTANCE,
            )
        return provider
