"""Implementing the LLM Interface class."""

from abc import ABC, abstractmethod


class LLMInterface(ABC):
    @abstractmethod
    def set_generation_model(self, generation_model_id: str):
        pass

    @abstractmethod
    def set_embedding_model(self, embedding_model_id: str):
        pass

    @abstractmethod
    def generate_text(
        self, messages: list[dict], max_output_tokens: int, temperature: float = None
    ):
        pass

    @abstractmethod
    def embed_text(self, text: str, doc_type: str):
        pass

    @abstractmethod
    def construct_prompt(self, prompt: str, role: str) -> list[dict]:
        pass
