import asyncio

from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.filters import Command

from nakormi_bot.entities.core_message import CoreMessage

router = Router(name='start_command')


@router.message(F.text, Command('run'))
async def start_command_handler(message: Message,
                                bot: Bot,
                                state: FSMContext):
    data = await state.get_data()

    # TODO: Реализовать всю эту логику в отдельном классе -> CoreContext
    # TODO: Добавить cleanup_list для удаления предыдущих сообщений (например, если нужно несколько сообщений)

    # Если предыдущее сообщение уже есть в диалоге
    if 'core_message' in data:
        core_message: CoreMessage = data['core_message']

        await bot.edit_message_text('Привет! ', chat_id=core_message.chat_id, message_id=core_message.message_id)

        return

    message = await message.answer('Привет! Это бот для удобного управления сетью "Накорми"')

    core_message = CoreMessage(chat_id=message.chat.id,
                               message_id=message.message_id,
                               date=message.date)

    await state.update_data(core_message=core_message)

    await asyncio.sleep(5)

    data = await state.get_data()
    c_m: CoreMessage = data['core_message']

    await bot.edit_message_text('Edited!!!', chat_id=c_m.chat_id, message_id=c_m.message_id)

# GET by Id
