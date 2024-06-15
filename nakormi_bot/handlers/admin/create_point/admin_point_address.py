from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from filters.regex_match_filter import RegexMatchFilter
from functional.core_context import CoreContext
from functional.phrases import Phrases
from handlers.registration.states.registration import RegistrationState
from keyboards.admin_keyboard import admin_point_keyboard
from handlers.admin.states.admin import PointAdminState

router = Router(name='admin_point_address')


@router.message(PointAdminState.waiting_for_address,
                F.text.len() >= 10,
                F.text.len() <= 255)
async def waiting_for_address(message: Message,
                              state: FSMContext,
                              context: CoreContext,
                              phrases: Phrases,
                              bot: Bot):
    core_message = context.get_message()

    await state.update_data(admin_point_address=message.text)

    await bot.edit_message_text(phrases['admin']['point_create']['coords']['text'],
                                chat_id=core_message.chat_id,
                                message_id=core_message.message_id,
                                parse_mode='HTML')
    await state.set_state(PointAdminState.waiting_for_coords)


@router.message(PointAdminState.waiting_for_address)
async def address_chosen_invalid_handler(message: Message,
                                      state: FSMContext,
                                      context: CoreContext,
                                      phrases: Phrases,
                                      bot: Bot):
    core_message = context.get_message()

    await bot.edit_message_text(phrases['admin']['point_create']['address']['invalid'],
                                chat_id=core_message.chat_id,
                                message_id=core_message.message_id,
                                parse_mode='HTML')
