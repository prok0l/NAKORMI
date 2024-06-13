from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from nakormi_bot.functional.core_context import CoreContext
from nakormi_bot.functional.core_message import CoreMessage
from nakormi_bot.functional.phrases import Phrases


class LanguageMiddleware(BaseMiddleware):
    # Используем словарь для языков, чтобы каждый раз не создавать новый объект
    # и не обращаться к файлам
    DEFINED_LANGUAGES = {
        'en': Phrases(f'phrases/phrases_en.json'),
        'ru': Phrases(f'phrases/phrases_ru.json'),
        'kz': Phrases(f'phrases/phrases_kz.json'),
        'fr': Phrases(f'phrases/phrases_fr.json'),
    }

    async def __call__(self,
                       handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
                       event: Message | CallbackQuery,
                       data: Dict[str, Any]
                       ) -> Any | None:
        state: FSMContext = data['state']
        bot: Bot = data['bot']
        context = await CoreContext.create(bot, state)

        if not context.language_defined():
            data['phrases'] = self.DEFINED_LANGUAGES['en']
            return await handler(event, data)

        # Add phrases to DI container
        data['phrases'] = self.DEFINED_LANGUAGES[context.get_language()]

        return await handler(event, data)
