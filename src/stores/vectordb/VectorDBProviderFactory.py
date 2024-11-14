"""Implementing the Vector DB Provider Factory class."""

from typing import Union
from .VectorDBConfig import VectorDBConfig
from ...helpers.config import Settings
from ...controllers.VectorDBController import VectorDBController


class VectorDBProviderFactory:
    def __init__(self, app_settings: Settings) -> None:
        self.app_settings = app_settings
        self.vectordb_controller = VectorDBController()
