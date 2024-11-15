"""Implementing the LLM Provider Factory class."""

from typing import Union
from .LLMConfig import LLMConfig
from helpers.config import Settings
from .providers.CoHereProvider import CoHereProvider
from .providers.OpenAIProvider import OpenAIProvider


class LLMProviderFactory:
    def __init__(self, app_settings: Settings) -> None:
        self.app_settings = app_settings

    def create_provider(
        self, provider_name: str
    ) -> Union[OpenAIProvider, CoHereProvider, None]:
        provider = None
        if provider_name == LLMConfig.OPENAI.value:
            provider = OpenAIProvider(
                api_key=self.app_settings.OPENAI_API_KEY,
                base_url=self.app_settings.OPENAI_BASE_URL,
                max_input_characters=self.app_settings.MAX_INPUT_CHARACTERS,
                max_output_tokens=self.app_settings.MAX_OUTPUT_TOKENS,
                temperature=self.app_settings.TEMPERATURE,
            )
        elif provider_name == LLMConfig.COHERE.value:
            provider = CoHereProvider(
                api_key=self.app_settings.COHERE_API_KEY,
                base_url=self.app_settings.COHERE_BASE_URL,
                max_input_characters=self.app_settings.MAX_INPUT_CHARACTERS,
                max_output_tokens=self.app_settings.MAX_OUTPUT_TOKENS,
                temperature=self.app_settings.TEMPERATURE,
            )
        return provider
