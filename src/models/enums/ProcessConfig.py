"""Defining data processing enumeration class."""

from enum import Enum


class ProcessConfig(Enum):
    TXT: str = ".txt"
    PDF: str = ".pdf"
