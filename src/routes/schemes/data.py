"""Implementing data processing request schema."""

from typing import Optional
from pydantic import BaseModel


class ProcessRequest(BaseModel):
    process_file_id: str
    process_chunk_size: Optional[int] = 100
    process_overlap_size: Optional[int] = 20
    process_do_reset: Optional[bool] = False
