"""Defining Base Controller class."""

import pathlib
from helpers.config import get_settings


class BaseController:
    def __init__(self) -> None:
        self.app_settings = get_settings()
        self.base_dir_path = pathlib.Path(__file__).parent.parent
        self.files_dir_path = self.base_dir_path.joinpath(pathlib.Path("assets").joinpath("files"))
