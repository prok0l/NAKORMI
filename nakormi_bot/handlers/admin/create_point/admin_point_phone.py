from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from filters.regex_match_filter import RegexMatchFilter
from functional.core_context import CoreContext
from functional.phrases import Phrases
from handlers.registration.states.registration import RegistrationState
from keyboards.admin_keyboard import admin_point_keyboard
from handlers.admin.states.admin import PointAdminState

router = Router(name='admin_point_phone')


@router.message(PointAdminState.waiting_for_phone,
                F.text.len() >= 12,
                F.text.len() <= 12,
                RegexMatchFilter(r'^\+[\d]{11}$'))
async def waiting_for_phone(message: Message,
                              state: FSMContext,
                              context: CoreContext,
                              phrases: Phrases,
                              bot: Bot):
    core_message = context.get_message()

    phone = message.text
    await state.update_data(admin_point_phone=phone)

    await bot.edit_message_text(phrases['admin']['point_create']['info']['text'],
                                chat_id=core_message.chat_id,
                                message_id=core_message.message_id,
                                parse_mode='HTML')
    await state.set_state(PointAdminState.waiting_for_info)


@router.message(PointAdminState.waiting_for_phone)
async def phone_chosen_invalid_handler(message: Message,
                                      state: FSMContext,
                                      context: CoreContext,
                                      phrases: Phrases,
                                      bot: Bot):
    core_message = context.get_message()

    await bot.edit_message_text(phrases['admin']['point_create']['phone']['invalid'],
                                chat_id=core_message.chat_id,
                                message_id=core_message.message_id,
                                parse_mode='HTML')
