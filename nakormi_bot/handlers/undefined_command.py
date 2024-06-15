from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from functional.core_context import CoreContext
from functional.core_message import CoreMessage
from functional.phrases import Phrases

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
                                    message_id=core_message.message_id,
                                    parse_mode='HTML')

        return

    new_message = await message.answer(phrases['undefined_command'], parse_mode='HTML')

    core_message = CoreMessage(chat_id=new_message.chat.id,
                               message_id=new_message.message_id,
                               telegram_id=message.from_user.id,
                               date=new_message.date)

    await context.update_message(core_message)
