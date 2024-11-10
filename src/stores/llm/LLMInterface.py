"""Implementing the LLM Interface class."""

from abc import ABC, abstractmethod


class LLMInterface(ABC):
    @abstractmethod
    def set_generation_model(self, generation_model_id: str) -> None:
        pass

    @abstractmethod
    def set_embedding_model(self, embedding_model_id: str, embedding_size: int) -> None:
        pass

    @abstractmethod
    def generate_text(
        self,
        prompt: str,
        chat_history: list = [],
        max_output_tokens: int = None,
        temperature: float = None,
    ):
        pass

    @abstractmethod
    def embed_text(self, text: str, doc_type: str = None):
        pass

    @abstractmethod
    def construct_prompt(self, prompt: str, role: str) -> dict:
        pass
