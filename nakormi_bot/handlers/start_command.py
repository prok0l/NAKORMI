from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from functional.core_context import CoreContext
from functional.core_message import CoreMessage
from functional.phrases import Phrases
from functional.representate_user import represent_user

from handlers.registration.states.registration import RegistrationState
from keyboards.language_keyboard import make_language_keyboard
from keyboards.main_menu_keyboard import main_menu_keyboard
from services.api.backend import Backend

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
    registered = 'registered' in data  #or backend.users.exists(message.from_user.id)

    # Если предыдущее сообщение уже есть в диалоге
    if context.message_exists() and registered:
        core_message = context.get_message()

        await bot.edit_message_text(phrases['start_command']['second'],
                                    chat_id=core_message.chat_id,
                                    message_id=core_message.message_id,
                                    parse_mode='HTML')

        return

    if not context.language_defined():
        keyboard = make_language_keyboard()
        new_message = await message.answer(phrases['language']['pick'],
                                           reply_markup=keyboard.as_markup(),
                                           parse_mode='HTML')

        core_message = CoreMessage(chat_id=new_message.chat.id,
                                   message_id=new_message.message_id,
                                   telegram_id=message.chat.id,
                                   date=new_message.date)

        await context.update_message(core_message)
        await state.set_state(RegistrationState.waiting_for_language)

        return

    if not await backend.users.exists(message.chat.id):
        return await bot.send_message(chat_id=message.chat.id,
                                      text=phrases['tg_id'].format(message.chat.id))
        return

    core_message = context.get_message()
    user = await backend.users.get(message.chat.id)
    if user.is_active:
        inventory = await backend.users.inventory(message.chat.id)
        keyboard = main_menu_keyboard(user)
        await bot.edit_message_text(represent_user(user=user, inventory=inventory, phrase=phrases),
                                    chat_id=core_message.chat_id,
                                    message_id=core_message.message_id,
                                    reply_markup=keyboard.as_markup(),
                                    parse_mode='HTML'
                                    )
        return

    await bot.edit_message_text(chat_id=core_message.chat_id,
                                message_id=core_message.message_id,
                                text=phrases['start_command']['first'],
                                parse_mode='HTML')

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
                                reply_markup=None,
                                parse_mode='HTML')

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
                                reply_markup=keyboard.as_markup(),
                                parse_mode='HTML')

    await state.set_state(RegistrationState.waiting_for_language)
