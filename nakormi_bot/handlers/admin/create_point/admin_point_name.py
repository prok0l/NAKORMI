from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from functional.core_context import CoreContext
from functional.phrases import Phrases
from handlers.admin.states.admin import PointAdminState

router = Router(name='admin_point_name')


@router.message(PointAdminState.waiting_for_name,
                F.text.len() >= 3,
                F.text.len() <= 100)
async def waiting_for_name(message: Message,
                           state: FSMContext,
                           context: CoreContext,
                           phrases: Phrases,
                           bot: Bot):
    core_message = context.get_message()

    await state.update_data(admin_point_name=message.text)
    await bot.edit_message_text(phrases['admin']['point_create']['address']['text'],
                                chat_id=core_message.chat_id,
                                message_id=core_message.message_id,
                                parse_mode='HTML')
    await state.set_state(PointAdminState.waiting_for_address)


@router.message(PointAdminState.waiting_for_name)
async def name_chosen_invalid_handler(message: Message,
                                      state: FSMContext,
                                      context: CoreContext,
                                      phrases: Phrases,
                                      bot: Bot):
    core_message = context.get_message()

    await bot.edit_message_text(phrases['admin']['point_create']['name']['invalid'],
                                chat_id=core_message.chat_id,
                                message_id=core_message.message_id,
                                parse_mode='HTML')
