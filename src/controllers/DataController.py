"""Defining Data Controller class."""

from fastapi import UploadFile
from .BaseController import BaseController


class DataController(BaseController):
    def __init__(self) -> None:
        super().__init__()
        self.file_scale = 1_048_576

    def validate_upload_file(self, file: UploadFile) -> tuple[bool, str]:
        result = True, "success"
        if file.content_type not in self.app_settings.FILE_ALLOWED_TYPES:
            result = False, "File type not supported"
        elif file.size > self.app_settings.FILE_MAX_SIZE * self.file_scale:
            result = False, "File size exceeds maximum"
        return result
