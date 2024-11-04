"""Defining Data Controller class."""

import pathlib
import aiofiles
from fastapi import UploadFile
from .BaseController import BaseController
from .ProjectController import ProjectController
from models.enums.ResponseSignal import ResponseSignal


class DataController(BaseController):
    def __init__(self) -> None:
        super().__init__()

    def validate_upload_file(self, file: UploadFile) -> tuple[bool, str]:
        result = True, ResponseSignal.FILE_PASSED_VALIDATION.value
        if file.content_type not in self.app_settings.FILE_ALLOWED_TYPES:
            result = False, ResponseSignal.FILE_TYPE_NOT_SUPPORTED.value
        elif file.size > self.app_settings.FILE_MAX_SIZE * self.file_scale:
            result = False, ResponseSignal.FILE_EXCEEDED_MAX_SIZE.value
        return result

    def get_unique_file_path(
        self, project_id: str, filename: str
    ) -> tuple[pathlib.Path, str]:
        project_path = ProjectController().get_project_path(project_id)
        clean_filename = self.get_clean_filename(filename)
        prefix = self.generate_random_string()
        file_id = f"{prefix}__{clean_filename}"
        file_path = project_path.joinpath(file_id)
        while file_path.exists():
            prefix = self.generate_random_string()
            file_id = f"{prefix}__{clean_filename}"
            file_path = project_path.joinpath(file_id)
        return file_path, file_id

    async def write_uploaded_file(
        self, file: UploadFile, file_path: pathlib.Path
    ) -> tuple[bool, str]:
        result = True, ResponseSignal.FILE_UPLOAD_SUCCEEDED.value
        try:
            async with aiofiles.open(file_path, "wb") as f:
                while chunk := await file.read(
                    size=self.app_settings.FILE_CHUNK_SIZE * self.file_scale
                ):  # walrus operator
                    await f.write(chunk)
        except Exception as e:
            result = False, ResponseSignal.FILE_UPLOAD_FAILED.value
        return result
