from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from filters.regex_match_filter import RegexMatchFilter
from functional.core_context import CoreContext
from functional.phrases import Phrases
from handlers.registration.states.registration import RegistrationState
from keyboards.admin_keyboard import admin_point_keyboard
from handlers.admin.states.admin import PointAdminState

router = Router(name='admin_point_coords')


@router.message(PointAdminState.waiting_for_coords,
                F.text.len() >= 10,
                F.text.len() <= 40,
                RegexMatchFilter(r'^\s*(-?\d{1,2}(?:\.\d+)?),\s*\s*(-?\d{1,3}(?:\.\d+)?)$'))
async def waiting_for_coords(message: Message,
                              state: FSMContext,
                              context: CoreContext,
                              phrases: Phrases,
                              bot: Bot):
    core_message = context.get_message()

    lat, lon = map(float, message.text.split(', '))
    await state.update_data(admin_point_lat=lat)
    await state.update_data(admin_point_lon=lon)

    await bot.edit_message_text(phrases['admin']['point_create']['phone']['text'],
                                chat_id=core_message.chat_id,
                                message_id=core_message.message_id,
                                parse_mode='HTML')
    await state.set_state(PointAdminState.waiting_for_phone)


@router.message(PointAdminState.waiting_for_coords)
async def coords_chosen_invalid_handler(message: Message,
                                      state: FSMContext,
                                      context: CoreContext,
                                      phrases: Phrases,
                                      bot: Bot):
    core_message = context.get_message()

    await bot.edit_message_text(phrases['admin']['point_create']['coords']['invalid'],
                                chat_id=core_message.chat_id,
                                message_id=core_message.message_id,
                                parse_mode='HTML')
