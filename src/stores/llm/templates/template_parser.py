"""Implementation of the Template Parser object."""

import pathlib
from typing import Union


class TemplateParser:
    def __init__(self, lang: str = None, default_lang: str = "english") -> None:
        self.current_dir_path = pathlib.Path(__file__).parent
        self.lang = lang
        self.default_lang = default_lang
        if self.lang is None:
            self.lang = self.default_lang

    def set_lang(self, lang: str) -> bool:
        result = False
        if lang is None:
            return result
        lang_path = self.current_dir_path.joinpath(
            pathlib.Path("locales").joinpath(lang)
        )
        if lang_path.exists():
            self.lang = lang
            result = True
        return result

    def get_template(self, group: str, key: str, vars: dict = {}) -> Union[str, None]:
        template = None
        lang = self.lang
        # ensure language path exists
        lang_path = self.current_dir_path.joinpath(
            pathlib.Path("locales").joinpath(lang)
        )
        if not lang_path.exists():
            lang = self.default_lang
            lang_path = self.current_dir_path.joinpath(
                pathlib.Path("locales").joinpath(lang)
            )
        # ensure group path exists for lang*
        if not lang_path.exists():
            # default lang templates are not defined
            return template
        lang_group_path = lang_path.joinpath(f"{group}.py")
        if not lang_group_path.exists():
            # group not defined for niether lang not default lang
            return template
        # get group template
        module = __import__(
            name=f"stores.llm.templates.locales.{lang}.{group}", fromlist=[group]
        )
        if not module:
            # group is empty
            return template
        # all is well at this point
        template = getattr(module, key).substitute(vars)
        return template
