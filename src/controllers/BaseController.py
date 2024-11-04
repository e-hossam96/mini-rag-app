"""Defining Base Controller class."""

import re
import string
import random
import pathlib
from helpers.config import get_settings


class BaseController:
    def __init__(self) -> None:
        self.app_settings = get_settings()
        self.file_scale = 1_048_576  # from MiBs to Bytes
        self.base_dir_path = pathlib.Path(__file__).parent.parent
        self.files_dir_path = self.base_dir_path.joinpath(
            pathlib.Path("assets").joinpath("files")
        )

    def generate_random_string(self, length: int = 12) -> str:
        population = string.ascii_lowercase + string.digits
        return "".join(random.choices(population=population, k=length))

    def get_clean_filename(self, filename) -> str:
        return re.sub(r"\W", r"_", filename)
