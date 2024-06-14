from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from nakormi_bot.filters.regex_match_filter import RegexMatchFilter
from nakormi_bot.functional.core_context import CoreContext
from nakormi_bot.functional.phrases import Phrases
from nakormi_bot.handlers.registration.states.registration import RegistrationState
from nakormi_bot.keyboards.skip_keyboard import make_skip_keyboard

router = Router(name='email_chosen')


async def proceed_to_image(state: FSMContext,
                           context: CoreContext,
                           phrases: Phrases,
                           bot: Bot):
    core_message = context.get_message()

    await bot.edit_message_text(phrases['registration']['email']['chosen'],
                                chat_id=core_message.chat_id,
                                message_id=core_message.message_id)

    reply_markup = make_skip_keyboard('skip_image', phrases)

    await bot.edit_message_reply_markup(chat_id=core_message.chat_id,
                                        message_id=core_message.message_id,
                                        reply_markup=reply_markup.as_markup())

    await state.set_state(RegistrationState.waiting_for_image)


@router.message(RegistrationState.waiting_for_email,
                F.text.len() >= 5,
                F.text.len() <= 150,
                RegexMatchFilter(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'))
async def email_chosen_handler(message: Message,
                               state: FSMContext,
                               context: CoreContext,
                               phrases: Phrases,
                               bot: Bot):
    email = message.text
    await state.update_data(email=email)

    await proceed_to_image(state, context, phrases, bot)


@router.callback_query(F.data.startswith('skip_email'))
async def email_skip_handler(callback_query: CallbackQuery,
                             state: FSMContext,
                             context: CoreContext,
                             phrases: Phrases,
                             bot: Bot):
    await proceed_to_image(state, context, phrases, bot)


@router.message(RegistrationState.waiting_for_email)
async def email_chosen_invalid_handler(message: Message,
                                       state: FSMContext,
                                       context: CoreContext,
                                       phrases: Phrases,
                                       bot: Bot):
    core_message = context.get_message()

    await bot.edit_message_text(phrases['registration']['email']['invalid'],
                                chat_id=core_message.chat_id,
                                message_id=core_message.message_id)
