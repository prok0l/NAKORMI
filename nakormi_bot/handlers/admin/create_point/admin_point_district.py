from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from filters.regex_match_filter import RegexMatchFilter
from functional.core_context import CoreContext
from functional.phrases import Phrases
from keyboards.admin_keyboard import admin_point_keyboard, admin_point_photo
from handlers.admin.states.admin import PointAdminState
from services.api.backend import Backend

router = Router(name='admin_point_district')


@router.message(PointAdminState.waiting_for_district,
                F.text.len() >= 2,
                F.text.len() <= 5)
async def admin_point_district(message: Message,
                               state: FSMContext,
                               context: CoreContext,
                               phrases: Phrases,
                               bot: Bot,
                               backend: Backend
                               ):
    data = await state.get_data()
    core_message = context.get_message()

    if message.text not in [x['name'] for x in data['districts']]:
        await bot.edit_message_text(phrases['admin']['point_create']['district']['invalid'],
                                    chat_id=core_message.chat_id,
                                    message_id=core_message.message_id,
                                    parse_mode='HTML')
        return
    await state.update_data(admin_point_district=message.text)

    keyboard = admin_point_photo()
    await bot.edit_message_text(phrases['admin']['point_create']['photo']['text'],
                                chat_id=core_message.chat_id,
                                message_id=core_message.message_id,
                                reply_markup=keyboard.as_markup(),
                                parse_mode='HTML')
    await state.set_state(PointAdminState.waiting_for_photo)

