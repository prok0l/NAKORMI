from typing import Dict, Any

from aiogram import Bot
from aiogram.fsm.context import FSMContext

from nakormi_bot.functional.core_message import CoreMessage


# TODO: Добавить cleanup_list для удаления предыдущих сообщений (например, если нужно несколько сообщений)
class CoreContext:
    CORE_MESSAGE_KEY: str = 'core_message'
    LANGUAGE_KEY: str = 'language'

    __create_key = object()

    def __init__(self, create_key: object):
        assert (create_key == CoreContext.__create_key,
                'CoreContext can be created only with CoreContext.create() method!')

        self.bot: Bot = None
        self.state: FSMContext = None
        self.data: Dict[str, Any] = None

    @classmethod
    async def create(cls, bot: Bot, state: FSMContext):
        self = cls(CoreContext.__create_key)
        self.bot = bot
        self.state = state
        self.data = await state.get_data()

        return self

    def message_exists(self) -> bool:
        return self.CORE_MESSAGE_KEY in self.data

    def get_message(self) -> CoreMessage:
        return self.data[self.CORE_MESSAGE_KEY]

    async def update_message(self, message: CoreMessage):
        await self.state.update_data({self.CORE_MESSAGE_KEY: message})

    def language_defined(self) -> bool:
        return self.LANGUAGE_KEY in self.data

    def get_language(self) -> str:
        return self.data[self.LANGUAGE_KEY]

    async def update_language(self, language: str):
        await self.state.update_data({self.LANGUAGE_KEY: language})
