"""Defining Response Signal enumeration class."""

from enum import Enum


class ResponseSignal(Enum):
    FILE_TYPE_NOT_SUPPORTED: str = "File_Type_Note_Supported"
    FILE_EXCEEDED_MAX_SIZE: str = "File_Exceeded_Maximum_SIZE"
    FILE_PASSED_VALIDATION: str = "File_Passed_Validation"
    FILE_UPLOAD_FAILED: str = "File_Upload_Failed"
    FILE_UPLOAD_SUCCEEDED: str = "File_Upload_Succeeded"
    FILE_PROCESS_SUCCEEDED: str = "File_Processing_Succeeded"
    FILE_PROCESS_FAILED: str = "File_Processing_Failed"
    NO_FILES_ERROR: str = "No_Files_Found_in_Database"
    NO_FILE_ERROR: str = "File_Not_Found_in_Database"
