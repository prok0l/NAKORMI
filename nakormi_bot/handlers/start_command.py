from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from nakormi_bot.functional.core_context import CoreContext
from nakormi_bot.functional.core_message import CoreMessage
from nakormi_bot.functional.phrases import Phrases

from nakormi_bot.handlers.registration.states.registration import RegistrationState
from nakormi_bot.keyboards.language_keyboard import make_language_keyboard
from nakormi_bot.services.api.backend import Backend

router = Router(name='start_command')


@router.message(F.text, Command('start'))
async def start_command_handler(message: Message,
                                bot: Bot,
                                state: FSMContext,
                                context: CoreContext,
                                phrases: Phrases,
                                backend: Backend):
    data = await state.get_data()

    # TODO: Возможно, стоит раскомментировать проверку на существование пользователя через бекенд
    # TODO: но пока что можно оставить и так, чтобы не нагружать
    registered = 'registered' in data or backend.users.exists(message.from_user.id)

    # Если предыдущее сообщение уже есть в диалоге
    if context.message_exists() and registered:
        core_message = context.get_message()

        await bot.edit_message_text(phrases['start_command']['second'],
                                    chat_id=core_message.chat_id,
                                    message_id=core_message.message_id)

        return

    if not context.language_defined():
        keyboard = make_language_keyboard()
        message = await message.answer(phrases['language']['pick'],
                                       reply_markup=keyboard.as_markup())

        core_message = CoreMessage(chat_id=message.chat.id,
                                   message_id=message.message_id,
                                   telegram_id=message.from_user.id,
                                   date=message.date)

        await context.update_message(core_message)
        await state.set_state(RegistrationState.waiting_for_language)

        return

    core_message = context.get_message()

    await bot.edit_message_text(chat_id=core_message.chat_id,
                                message_id=core_message.message_id,
                                text=phrases['start_command']['first'])

    await state.set_state(RegistrationState.waiting_for_name)


@router.callback_query(RegistrationState.waiting_for_language,
                       F.data.startswith('language_'))
async def language_chosen(callback: CallbackQuery,
                          state: FSMContext,
                          context: CoreContext,
                          phrases: Phrases,
                          bot: Bot):
    core_message = context.get_message()

    language = callback.data.split('_')[-1]
    await context.update_language(language)

    await bot.edit_message_text(phrases['language']['picked'],
                                chat_id=core_message.chat_id,
                                message_id=core_message.message_id,
                                reply_markup=None)

    await state.set_state(None)


@router.message(RegistrationState.waiting_for_language)
async def language_chosen_invalid(message: Message,
                                  state: FSMContext,
                                  context: CoreContext,
                                  bot: Bot,
                                  phrases: Phrases):
    core_message = context.get_message()

    keyboard = make_language_keyboard()
    await bot.edit_message_text(phrases['language']['invalid'],
                                chat_id=core_message.chat_id,
                                message_id=core_message.message_id,
                                reply_markup=keyboard.as_markup())

    await state.set_state(RegistrationState.waiting_for_language)
