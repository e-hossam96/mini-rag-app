"""Implementation of Vector DB Controller class."""

import pathlib
from .BaseController import BaseController


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
