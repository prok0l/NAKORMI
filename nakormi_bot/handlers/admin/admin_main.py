from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from filters.regex_match_filter import RegexMatchFilter
from functional.core_context import CoreContext
from functional.phrases import Phrases
from keyboards.admin_keyboard import admin_keyboard

router = Router(name='admin_main')


@router.callback_query(F.data.startswith('admin_main'))
async def edit_profile_handler(callback_query: CallbackQuery,
                               state: FSMContext,
                               context: CoreContext,
                               phrases: Phrases,
                               bot: Bot):
    core_message = context.get_message()

    keyboard = admin_keyboard()

    await bot.edit_message_text(phrases['admin']['main'],
                                chat_id=core_message.chat_id,
                                message_id=core_message.message_id,
                                reply_markup=keyboard.as_markup(),
                                parse_mode='HTML')




