"""Defining Data Controller class."""

from fastapi import UploadFile
from .BaseController import BaseController
from models.enums.ResponseSignal import ResponseSignal


class DataController(BaseController):
    def __init__(self) -> None:
        super().__init__()
        self.file_scale = 1_048_576

    def validate_upload_file(self, file: UploadFile) -> tuple[bool, str]:
        result = True, ResponseSignal.FILE_PASSED_VALIDATION.value
        if file.content_type not in self.app_settings.FILE_ALLOWED_TYPES:
            result = False, ResponseSignal.FILE_TYPE_NOT_SUPPORTED.value
        elif file.size > self.app_settings.FILE_MAX_SIZE * self.file_scale:
            result = False, ResponseSignal.FILE_EXCEEDED_MAX_SIZE.value
        return result
