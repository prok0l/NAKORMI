from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from filters.regex_match_filter import RegexMatchFilter
from functional.core_context import CoreContext
from functional.phrases import Phrases
from handlers.edit_profile.states.profile_edit import ProfileEditState
from handlers.registration.states.registration import RegistrationState
from keyboards.redirect_keyboard import make_redirect_keyboard
from keyboards.skip_keyboard import make_skip_keyboard

from keyboards.edit_profile_keyboard import make_edit_profile_keyboard
from services.api.backend import Backend

router = Router(name='edit_phone')


@router.callback_query(F.data.startswith('edit_phone'))
async def edit_phone_handler(callback_query: CallbackQuery,
                             state: FSMContext,
                             context: CoreContext,
                             phrases: Phrases,
                             backend: Backend,
                             bot: Bot):
    core_message = context.get_message()

    await bot.edit_message_text(phrases['edit_profile']['options'][2]['text'],
                                chat_id=core_message.chat_id,
                                message_id=core_message.message_id,
                                parse_mode='HTML')

    await state.set_state(ProfileEditState.waiting_for_phone)


@router.message(ProfileEditState.waiting_for_phone,
                F.text.len() >= 11,
                F.text.len() <= 15,
                RegexMatchFilter(r'^\+\d{11}$'))
async def phone_chosen_handler(message: Message,
                               state: FSMContext,
                               phrases: Phrases,
                               context: CoreContext,
                               backend: Backend,
                               bot: Bot):
    core_message = context.get_message()

    user = await backend.users.get(core_message.telegram_id)

    phone = message.text
    user.phone = phone

    await backend.users.update(user)

    await state.update_data(phone=phone)

    core_message = context.get_message()

    await bot.edit_message_text(phrases['edit_profile']['options'][2]['correct'],
                                chat_id=core_message.chat_id,
                                message_id=core_message.message_id,
                                parse_mode='HTML')

    await state.set_state(None)

    reply_markup = make_redirect_keyboard(destination_callback='menu',
                                          text=phrases['edit_profile']['back'])

    await bot.edit_message_reply_markup(chat_id=core_message.chat_id,
                                        message_id=core_message.message_id,
                                        reply_markup=reply_markup.as_markup())


@router.message(ProfileEditState.waiting_for_phone)
async def phone_chosen_invalid_handler(message: Message,
                                       state: FSMContext,
                                       context: CoreContext,
                                       phrases: Phrases,
                                       bot: Bot):
    core_message = context.get_message()

    await bot.edit_message_text(phrases['edit_profile']['options'][2]['invalid'],
                                chat_id=core_message.chat_id,
                                message_id=core_message.message_id,
                                parse_mode='HTML')
