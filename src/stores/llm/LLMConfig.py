"""Implementing the LLM Configurtions enumeration class."""

from enum import Enum


class LLMConfig(Enum):
    OPENAI: str = "openai"
    COHERE: str = "cohere"


class OpenAIConfig(Enum):
    SYSTEM: str = "system"
    USER: str = "user"
    AI_AGENT: str = "assistant"
