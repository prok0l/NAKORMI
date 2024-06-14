from aiogram import Router, F, Bot
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext

from filters.regex_match_filter import RegexMatchFilter
from functional.core_context import CoreContext
from functional.phrases import Phrases
from handlers.registration.states.registration import RegistrationState

router = Router(name='name_chosen')


@router.message(RegistrationState.waiting_for_name,
                F.text.len() >= 3,
                F.text.len() <= 150,
                RegexMatchFilter(r'^[А-ЯЁ][а-яё]* [А-ЯЁ][а-яё]*$'))
async def name_chosen_handler(message: Message,
                              state: FSMContext,
                              phrases: Phrases,
                              context: CoreContext,
                              bot: Bot):
    name = message.text
    await state.update_data(name=name)

    core_message = context.get_message()

    await bot.edit_message_text(phrases['registration']['name']['chosen'].format(name),
                                chat_id=core_message.chat_id,
                                message_id=core_message.message_id)

    await state.set_state(RegistrationState.waiting_for_phone)


@router.message(RegistrationState.waiting_for_name)
async def name_chosen_invalid_handler(message: Message,
                                      state: FSMContext,
                                      context: CoreContext,
                                      phrases: Phrases,
                                      bot: Bot):
    core_message = context.get_message()

    await bot.edit_message_text(phrases['registration']['name']['invalid'],
                                chat_id=core_message.chat_id,
                                message_id=core_message.message_id)
