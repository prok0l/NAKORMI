from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from nakormi_bot.entities.core_message import CoreMessage


class SingleMessageMiddleware(BaseMiddleware):
    async def __call__(self,
                       handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
                       event: Message,
                       data: Dict[str, Any]
                       ) -> Any | None:
        state: FSMContext = data['state']
        bot: Bot = data['bot']

        state_data = await state.get_data()

        if 'core_message' in state_data:
            core_message: CoreMessage = state_data['core_message']

            # Если прошло 5 секунд с момента последнего сообщения
            if (event.date - core_message.date).total_seconds() > 5:
                await bot.delete_message(chat_id=core_message.chat_id, message_id=core_message.message_id)

                await self.send_revert_state_message(state, bot, event)

        # Удаление сообщения пользователя
        await bot.delete_message(chat_id=event.chat.id, message_id=event.message_id)

        return await handler(event, data)

    @staticmethod
    async def send_revert_state_message(state: FSMContext, bot: Bot, event: Message):
        await state.set_state(None)

        new_message = await bot.send_message(event.chat.id, 'Нажми /start, чтобы вернуться в меню')

        await state.update_data(core_message=CoreMessage(new_message.chat.id,
                                                         new_message.message_id,
                                                         new_message.date))

