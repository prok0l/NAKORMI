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

router = Router(name='edit_image')


@router.callback_query(F.data.startswith('edit_image'))
async def edit_image_handler(callback_query: CallbackQuery,
                             state: FSMContext,
                             context: CoreContext,
                             phrases: Phrases,
                             backend: Backend,
                             bot: Bot):
    core_message = context.get_message()

    await bot.edit_message_text(phrases['edit_profile']['options'][3]['text'],
                                chat_id=core_message.chat_id,
                                message_id=core_message.message_id,
                                parse_mode='HTML')

    await state.set_state(ProfileEditState.waiting_for_image)


@router.message(ProfileEditState.waiting_for_image,
                F.photo)
async def image_chosen_handler(message: Message,
                               state: FSMContext,
                               phrases: Phrases,
                               context: CoreContext,
                               backend: Backend,
                               bot: Bot):
    core_message = context.get_message()

    user = await backend.users.get(core_message.telegram_id)

    obj = message.photo[-1]
    file = await message.bot.download(file=obj.file_id, destination="images\\avatar.png")
    with open("images\\avatar.png", "rb") as f:
        file_id = await backend.users.upload_avatar(file=f, user_id=core_message.telegram_id)

    await backend.users.update(user)

    core_message = context.get_message()

    await bot.edit_message_text(phrases['edit_profile']['options'][3]['correct'],
                                chat_id=core_message.chat_id,
                                message_id=core_message.message_id,
                                parse_mode='HTML')

    await state.set_state(None)

    reply_markup = make_redirect_keyboard(destination_callback='menu',
                                          text=phrases['edit_profile']['back'])

    await bot.edit_message_reply_markup(chat_id=core_message.chat_id,
                                        message_id=core_message.message_id,
                                        reply_markup=reply_markup.as_markup())


@router.message(ProfileEditState.waiting_for_image)
async def image_chosen_invalid_handler(message: Message,
                                       state: FSMContext,
                                       context: CoreContext,
                                       phrases: Phrases,
                                       bot: Bot):
    core_message = context.get_message()

    await bot.edit_message_text(phrases['edit_profile']['options'][3]['invalid'],
                                chat_id=core_message.chat_id,
                                message_id=core_message.message_id,
                                parse_mode='HTML')
