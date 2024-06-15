from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from filters.regex_match_filter import RegexMatchFilter
from functional.core_context import CoreContext
from functional.phrases import Phrases
from handlers.registration.states.registration import RegistrationState
from keyboards.skip_keyboard import make_skip_keyboard

from nakormi_bot.keyboards.edit_profile_keyboard import make_edit_profile_keyboard

router = Router(name='email_chosen')


@router.callback_query(F.data.startswith('edit_profile'))
async def edit_profile_handler(callback_query: CallbackQuery,
                               state: FSMContext,
                               context: CoreContext,
                               phrases: Phrases,
                               bot: Bot):
    core_message = context.get_message()

    await bot.edit_message_text(phrases['edit_profile']['info'],
                                chat_id=core_message.chat_id,
                                message_id=core_message.message_id,
                                parse_mode='HTML')

    reply_markup = make_edit_profile_keyboard(phrases)

    await bot.edit_message_reply_markup(chat_id=core_message.chat_id,
                                        message_id=core_message.message_id,
                                        reply_markup=reply_markup.as_markup())
