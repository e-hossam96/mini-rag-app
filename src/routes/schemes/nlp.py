"""Implementing NLP requests schemas."""

from typing import Optional
from pydantic import BaseModel


class PushRequest(BaseModel):
    do_reset: Optional[bool] = False


class SearchRequest(BaseModel):
    text: str
    limit: Optional[int] = 5
