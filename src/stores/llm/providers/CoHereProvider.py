"""Impolementing CoHere Provider class."""

import logging
import cohere
from typing import Union
from ..LLMConfig import LLMConfig, CoHereConfig
from ..LLMInterface import LLMInterface


class CoHereProvider(LLMInterface):
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
        self.client = cohere.ClientV2(api_key=self.api_key, base_url=self.base_url)
        self.logger = logging.getLogger(__name__)

    def set_generation_model(self, generation_model_id: str) -> None:
        self.generation_model_id = generation_model_id

    def set_embedding_model(self, embedding_model_id: str, embedding_size: int) -> None:
        self.embedding_model_id = embedding_model_id
        self.embedding_size = embedding_size
