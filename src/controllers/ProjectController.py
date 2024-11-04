"""Implementation of Project Controller class."""

import pathlib
from .BaseController import BaseController


class ProjectController(BaseController):
    def __init__(self) -> None:
        super().__init__()

    def get_project_path(self, project_id: str) -> pathlib.Path:
        project_path = self.files_dir_path.joinpath(project_id)
        # take care when using parents in mkdir
        # we are sure parents exist. we will set it to True
        # in case project has nested directories
        project_path.mkdir(parents=True, exist_ok=True)
        return project_path
