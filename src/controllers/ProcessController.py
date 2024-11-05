"""Implementing data processing controller class."""

import pathlib
from typing import Union
from .BaseController import BaseController
from .ProjectController import ProjectController
from models.enums.ProcessConfig import ProcessConfig
from langchain_core.documents.base import Document
from langchain_community.document_loaders import TextLoader, PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter


class ProcessController(BaseController):
    def __init__(self, project_id: str) -> None:
        super().__init__()
        self.project_id = project_id
        self.project_path = ProjectController().get_project_path(self.project_id)

    def get_file_ext(self, process_file_id: str) -> str:
        return pathlib.Path(process_file_id).suffix

    def get_file_loader(
        self, process_file_id: str
    ) -> Union[TextLoader, PyMuPDFLoader, None]:
        file_ext = self.get_file_ext(process_file_id)
        file_path = self.project_path.joinpath(process_file_id)
        file_loader = None
        if file_ext == ProcessConfig.TXT.value:
            file_loader = TextLoader(file_path, encoding="utf-8")
        elif file_ext == ProcessConfig.PDF.value:
            file_loader = PyMuPDFLoader(str(file_path))
        return file_loader

    def get_file_content(self, process_file_id: str) -> Union[list[Document], None]:
        file_loader = self.get_file_loader(process_file_id)
        file_content = None
        if file_loader is not None:
            file_content = file_loader.load()
        return file_content

    def process_file_content(
        self, file_content: list[Document], chunk_size: int, overlap_size: int
    ) -> list[Document]:
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            overlap_size=overlap_size,
        )
        texts = [doc.page_content for doc in file_content]
        metadata = [doc.metadata for doc in file_content]
        chunks = text_splitter.create_documents(texts=texts, metadatas=metadata)
        return chunks
