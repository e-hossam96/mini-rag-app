"""Defining Response Signal enumeration class."""

from enum import Enum


class ResponseConfig(Enum):
    FILE_TYPE_NOT_SUPPORTED: str = "File_Type_Note_Supported"
    FILE_EXCEEDED_MAX_SIZE: str = "File_Exceeded_Maximum_SIZE"
    FILE_PASSED_VALIDATION: str = "File_Passed_Validation"
    FILE_UPLOAD_FAILED: str = "File_Upload_Failed"
    FILE_UPLOAD_SUCCEEDED: str = "File_Upload_Succeeded"
    FILE_PROCESS_SUCCEEDED: str = "File_Processing_Succeeded"
    FILE_PROCESS_FAILED: str = "File_Processing_Failed"
    NO_FILES_ERROR: str = "No_Files_Found_in_Database"
    NO_FILE_ERROR: str = "File_Not_Found_in_Database"
    NO_CHUNKS_ERROR: str = "No_Chunks_Found_in_Database"
    EMBEDDING_CHUNKS_FAILED: str = "Chunks_Embedding_Falied"
    VECTORDB_INDEXING_FALIED: str = "Indexing_VectorDB_Falied"
    VECTORDB_INDEXING_SUCCEEDED: str = "Indexing_VectorDB_Succeeded"
    VECTORDB_COLLECTION__INFO_RETRIEVED: str = "VectorDB_Collection_Info_Retrieved"
    VECTORDB_COLLECTION__INFO_MISSING: str = "VectorDB_Collection_Info_Missing"
    VECTORDB_INDEX_SEARCH_SUCCEEDED: str = "VectorDB_Index_Search_Succeeded"
    VECTORDB_INDEX_SEARCH_FAILED: str = "VectorDB_Index_Search_Failed"
    RAG_ANSWER_FAILED: str = "RAG_Answer_Failed"
    RAG_ANSWER_SUCCEEDED: str = "RAG_Answer_Succeeded"
