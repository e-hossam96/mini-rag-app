"""Implementing the LLM Configurtions enumeration class."""

from enum import Enum


class LLMConfig(Enum):
    OPENAI: str = "openai"
    COHERE: str = "cohere"


class OpenAIConfig(Enum):
    SYSTEM: str = "system"
    USER: str = "user"
    AI_AGENT: str = "assistant"


class CoHereV2Config(Enum):
    SYSTEM: str = "system"
    USER: str = "user"
    AI_AGENT: str = "assistant"
    DOC: str = "search_document"
    QUERY: str = "search_query"


class DocTypeConfig(Enum):
    DOC: str = "document"
    QUERY: str = "query"
