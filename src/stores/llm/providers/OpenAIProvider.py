"""Impolementing OpenAI Provider class."""

import logging
from openai import OpenAI
from ..LLMInterface import LLMInterface


class OpenAIProvider(LLMInterface):
    def __init__(
        self,
        api_key: str,
        base_url: str = None,
        max_input_characters: int = 1000,
        max_output_tokens: int = 32,
        temperature: float = 0.01,
    ) -> None:
        # defaults
        self.api_key = api_key
        self.base_url = base_url
        self.max_input_characters = max_input_characters
        self.max_output_tokens = max_output_tokens
        self.temperature = temperature
        # runtime changables
        self.generation_model_id = None
        self.embedding_model_id = None
        self.embedding_size = None
        # define client
        self.client = OpenAI(api_key=self.api_key, base_url=self.base_url)
        self.logger = logging.getLogger(__name__)
