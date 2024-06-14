from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from functional.core_context import CoreContext
from functional.core_message import CoreMessage
from functional.phrases import Phrases


class SingleMessageMiddleware(BaseMiddleware):
    async def __call__(self,
                       handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
                       event: Message | CallbackQuery,
                       data: Dict[str, Any]
                       ) -> Any | None:
        state: FSMContext = data['state']
        bot: Bot = data['bot']
        phrases: Phrases = data['phrases']
        context = await CoreContext.create(bot, state)
        event_instance = event
        user_id = event.from_user.id

        # Add context to DI container
        data['context'] = context

        event_is_callback = isinstance(event, CallbackQuery)

        # Если нам пришел ответ из CallbackQuery
        if event_is_callback:
            event_instance = event.message

        if context.message_exists():
            core_message = context.get_message()

            # Если прошло 48 часов с момента последнего сообщения, то удаляем его
            if (event_instance.date - core_message.date).total_seconds() > 2 * 24 * 60 * 60:
                await bot.delete_message(chat_id=core_message.chat_id, message_id=core_message.message_id)

                await self.send_revert_state_message(state, bot, event_instance, context, phrases, user_id)

        # Удаление сообщения пользователя
        if not event_is_callback:
            await bot.delete_message(chat_id=event_instance.chat.id, message_id=event_instance.message_id)

        return await handler(event, data)

    @staticmethod
    async def send_revert_state_message(state: FSMContext,
                                        bot: Bot,
                                        event: Message,
                                        context: CoreContext,
                                        phrases: Phrases,
                                        user_id: int) -> None:
        await state.set_state(None)

        new_message = await bot.send_message(event.chat.id, phrases['return_to_menu'])

        core_message = CoreMessage(new_message.chat.id,
                                   new_message.message_id,
                                   user_id,
                                   new_message.date)

        await context.update_message(core_message)

