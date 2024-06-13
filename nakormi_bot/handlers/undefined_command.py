from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from nakormi_bot.functional.core_context import CoreContext
from nakormi_bot.functional.core_message import CoreMessage
from nakormi_bot.functional.phrases import Phrases

router = Router(name='undefined_command')


@router.message(F.text)
async def undefined_command_handler(message: Message,
                                    bot: Bot,
                                    state: FSMContext,
                                    context: CoreContext,
                                    phrases: Phrases):

    # Если предыдущее сообщение уже есть в диалоге
    if context.message_exists():
        core_message = context.get_message()

        await bot.edit_message_text(phrases['undefined_command'],
                                    chat_id=core_message.chat_id,
                                    message_id=core_message.message_id)

        return

    message = await message.answer(phrases['undefined_command'])

    core_message = CoreMessage(chat_id=message.chat.id,
                               message_id=message.message_id,
                               telegram_id=message.from_user.id,
                               date=message.date)

    await context.update_message(core_message)
