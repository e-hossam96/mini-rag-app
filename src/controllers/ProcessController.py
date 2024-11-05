"""Implementing data processing controller class."""

import pathlib
from .BaseController import BaseController
from .ProjectController import ProjectController


class ProcessController(BaseController):
    def __init__(self, project_id: str) -> None:
        super().__init__()
        self.project_id = project_id
        self.project_path = ProjectController().get_project_path(self.project_id)

    def get_file_ext(self, process_file_id: str) -> str:
        return pathlib.Path(process_file_id).suffix
