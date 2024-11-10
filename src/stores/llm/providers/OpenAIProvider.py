"""Impolementing OpenAI Provider class."""

import logging
from openai import OpenAI
from typing import Union
from ..LLMConfig import LLMConfig, OpenAIConfig
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

    def set_generation_model(self, generation_model_id: str) -> None:
        self.generation_model_id = generation_model_id

    def set_embedding_model(self, embedding_model_id: str, embedding_size: int) -> None:
        self.embedding_model_id = embedding_model_id
        self.embedding_size = embedding_size

    def process_prompt(self, prompt: str) -> str:
        if len(prompt) > self.max_input_characters:
            self.logger.warning("Prompt is longer than expected.")
            prompt = prompt[: self.max_input_characters].strip()
        return prompt

    def construct_prompt(self, prompt: str, role: str) -> dict:
        return {"role": role, "content": self.process_prompt(prompt)}

    def generate_text(
        self,
        prompt: str,
        chat_history: list = [],
        max_output_tokens: int = None,
        temperature: float = None,
    ) -> Union[str, None]:
        # ensure client and model id are set
        if self.client is None:
            self.logger.error(f"{LLMConfig.OPENAI.value} was not set.")
            return None
        if self.generation_model_id is None:
            self.logger.error(f"{LLMConfig.OPENAI.value} generation model id not set.")
            return None
        # ensure generation parameters are set
        if max_output_tokens is None:
            max_output_tokens = self.max_output_tokens
        if temperature is None:
            temperature = self.temperature
        # send prompt to chat endpoint
        chat_history.append(self.construct_prompt(prompt, OpenAIConfig.USER.value))
        resp = self.client.chat.completions.create(
            model=self.generation_model_id,
            messages=chat_history,
            max_completion_tokens=max_output_tokens,
            temperature=temperature,
        )
        # validate response
        if (
            resp is None
            or resp.choices is None
            or len(resp.choices) == 0
            or resp.choices[0].message is None
        ):
            self.logger.error(f"{LLMConfig.OPENAI.value} response generation failed.")
            return None
        return resp.choices[0].message.content

    def embed_text(self, text: str, doc_type: str = None) -> Union[list[float], None]:
        # ensure client and model id are set
        if self.client is None:
            self.logger.error(f"{LLMConfig.OPENAI.value} was not set.")
            return None
        if self.embedding_model_id is None:
            self.logger.error(f"{LLMConfig.OPENAI.value} embedding model id not set.")
            return None
        # send text to embedding endpoint
        resp = self.client.embeddings.create(model=self.embedding_model_id, input=text)
        if (
            resp is None
            or resp.data is None
            or len(resp.data) == 0
            or resp.data[0].embedding is None
        ):
            self.logger.error(f"{LLMConfig.OPENAI.value} embedding response failed.")
            return None
        return resp.data[0].embedding
