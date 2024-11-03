"""Defining Base Controller class."""

from helpers.config import get_settings


class BaseController:
    def __init__(self) -> None:
        self.app_settings = get_settings()
