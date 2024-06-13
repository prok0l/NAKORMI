from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from nakormi_bot.functional.core_context import CoreContext
from nakormi_bot.functional.phrases import Phrases
from nakormi_bot.handlers.registration.states.registration import RegistrationState
from nakormi_bot.keyboards.skip_keyboard import make_skip_keyboard

router = Router(name='phone_chosen')


@router.message(RegistrationState.waiting_for_phone,
                F.text.len() >= 11,
                F.text.len() <= 15)
async def phone_chosen_handler(message: Message,
                               state: FSMContext,
                               context: CoreContext,
                               phrases: Phrases,
                               bot: Bot):
    phone = message.text
    await state.update_data(phone=phone)

    core_message = context.get_message()

    await bot.edit_message_text(phrases['registration']['phone']['chosen'],
                                chat_id=core_message.chat_id,
                                message_id=core_message.message_id)

    reply_markup = make_skip_keyboard('skip_email', phrases)

    await bot.edit_message_reply_markup(chat_id=core_message.chat_id,
                                        message_id=core_message.message_id,
                                        reply_markup=reply_markup.as_markup())

    await state.set_state(RegistrationState.waiting_for_email)


@router.message(RegistrationState.waiting_for_phone)
async def phone_chosen_invalid_handler(message: Message,
                                       state: FSMContext,
                                       context: CoreContext,
                                       phrases: Phrases,
                                       bot: Bot):
    core_message = context.get_message()

    await bot.edit_message_text(phrases['registration']['phone']['invalid'],
                                chat_id=core_message.chat_id,
                                message_id=core_message.message_id)
