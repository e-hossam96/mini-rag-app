"""Defining Response Signal enumeration class."""

from enum import Enum


class ResponseSignal(Enum):
    FILE_TYPE_NOT_SUPPORTED: str = "File_Type_Note_Supported"
    FILE_EXCEEDED_MAX_SIZE: str = "File_Exceeded_Maximum_SIZE"
    FILE_PASSED_VALIDATION: str = "File_Passed_Validation"
    FILE_UPLOAD_FAILED: str = "File_Upload_Failed"
    FILE_UPLOAD_SUCCEEDED: str = "File_Upload_Succeeded"