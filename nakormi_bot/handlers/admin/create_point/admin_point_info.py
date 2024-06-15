from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from filters.regex_match_filter import RegexMatchFilter
from functional.core_context import CoreContext
from functional.phrases import Phrases
from handlers.registration.states.registration import RegistrationState
from keyboards.admin_keyboard import admin_point_keyboard
from handlers.admin.states.admin import PointAdminState
from services.api.backend import Backend

router = Router(name='admin_point_info')


@router.message(PointAdminState.waiting_for_info,
                F.text.len() >= 3,
                F.text.len() <= 255)
async def waiting_for_info(message: Message,
                           state: FSMContext,
                           context: CoreContext,
                           phrases: Phrases,
                           bot: Bot,
                           backend: Backend):
    core_message = context.get_message()

    info = message.text
    await state.update_data(admin_point_info=info)
    districts = await backend.main.get_districts(core_message.telegram_id)
    await state.update_data(districts=districts)
    msg_text = (phrases['admin']['point_create']['district']['text'] +
                phrases['admin']['point_create']['district']['second']) + ", ".join(x['name'] for x in districts)

    await bot.edit_message_text(msg_text,
                                chat_id=core_message.chat_id,
                                message_id=core_message.message_id,
                                parse_mode='HTML')
    await state.set_state(PointAdminState.waiting_for_district)


@router.message(PointAdminState.waiting_for_info)
async def info_chosen_invalid_handler(message: Message,
                                      state: FSMContext,
                                      context: CoreContext,
                                      phrases: Phrases,
                                      bot: Bot):
    core_message = context.get_message()

    await bot.edit_message_text(phrases['admin']['point_create']['info']['invalid'],
                                chat_id=core_message.chat_id,
                                message_id=core_message.message_id,
                                parse_mode='HTML')
