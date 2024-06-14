import re
from typing import Union

from aiogram.enums import ContentType
from aiogram.filters import BaseFilter
from aiogram.types import Message


class RegexMatchFilter(BaseFilter):
    def __init__(self, regex: str):
        self.regex_pattern = regex

    async def __call__(self, message: Message) -> bool:
        return re.match(self.regex_pattern, message.text) is not None
