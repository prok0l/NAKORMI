from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from filters.regex_match_filter import RegexMatchFilter
from functional.core_context import CoreContext
from functional.phrases import Phrases
from handlers.registration.states.registration import RegistrationState
from keyboards.skip_keyboard import make_skip_keyboard

from services.api.backend import Backend

router = Router(name='phone_chosen')


@router.message(RegistrationState.waiting_for_phone,
                F.text.len() >= 11,
                F.text.len() <= 15,
                RegexMatchFilter(r'^\+\d{11}$'))
async def phone_chosen_handler(message: Message,
                               state: FSMContext,
                               context: CoreContext,
                               phrases: Phrases,
                               bot: Bot,
                               backend: Backend):
    phone = message.text
    await state.update_data(phone=phone)

    core_message = context.get_message()

    districts = await backend.main.get_districts(user_id=core_message.telegram_id)
    districts_lst = [x['name'] for x in districts]
    await state.update_data(districts=districts_lst)

    msg_text = phrases['registration']['phone']['chosen'] + ", ".join(districts_lst)

    await bot.edit_message_text(msg_text,
                                chat_id=core_message.chat_id,
                                message_id=core_message.message_id,
                                parse_mode='HTML')

    await state.set_state(RegistrationState.waiting_for_district)


@router.message(RegistrationState.waiting_for_phone)
async def phone_chosen_invalid_handler(message: Message,
                                       state: FSMContext,
                                       context: CoreContext,
                                       phrases: Phrases,
                                       bot: Bot):
    core_message = context.get_message()

    await bot.edit_message_text(phrases['registration']['phone']['invalid'],
                                chat_id=core_message.chat_id,
                                message_id=core_message.message_id,
                                parse_mode='HTML')
