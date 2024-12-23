"""Impolementing CoHere Provider class."""

import logging
import cohere
from typing import Union
from ..LLMConfig import LLMConfig, CoHereV2Config, DocTypeConfig
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
        self.config = CoHereV2Config
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
            self.logger.error(f"{LLMConfig.COHERE.value} was not set.")
            return None
        if self.generation_model_id is None:
            self.logger.error(
                f"{LLMConfig.COHERE.value} generation model id was not set."
            )
            return None
        # ensure generation parameters are set
        if max_output_tokens is None:
            max_output_tokens = self.max_output_tokens
        if temperature is None:
            temperature = self.temperature
        # send prompt to chat endpoint
        chat_history.append(self.construct_prompt(prompt, CoHereV2Config.USER.value))
        resp = self.client.chat(
            model=self.generation_model_id,
            messages=chat_history,
            max_tokens=max_output_tokens,
            temperature=temperature,
        )
        # validate response
        if (
            resp is None
            or resp.message is None
            or resp.message.content is None
            or len(resp.message.content) == 0
        ):
            self.logger.error(f"{LLMConfig.COHERE.value} generation response failed.")
            return None
        return resp.message.content[0].text

    def embed_text(self, text: str, doc_type: str = None) -> Union[list[float], None]:
        # ensure client and model id are set
        if self.client is None:
            self.logger.error(f"{LLMConfig.COHERE.value} was not set.")
            return None
        if self.embedding_model_id is None:
            self.logger.error(
                f"{LLMConfig.COHERE.value} embedding model id was not set."
            )
            return None
        # send text to embedding endpoint
        if doc_type is None or doc_type == DocTypeConfig.DOC.value:
            # set default to document
            doc_type = CoHereV2Config.DOC.value
        elif doc_type == DocTypeConfig.QUERY.value:
            doc_type = CoHereV2Config.QUERY.value
        else:
            # handle the case when input type is unknown
            self.logger.error(f"{LLMConfig.COHERE.value} unknown input type.")
            return None
        resp = self.client.embed(
            model=self.embedding_model_id,
            texts=[self.process_prompt(text)],
            input_type=doc_type,
            embedding_types=["float"],
        )
        if (
            resp is None
            or resp.embeddings is None
            or resp.embeddings.float_ is None
            or len(resp.embeddings.float_) == 0
        ):
            self.logger.error(f"{LLMConfig.COHERE.value} embedding response failed.")
            return None
        return resp.embeddings.float_[0]
