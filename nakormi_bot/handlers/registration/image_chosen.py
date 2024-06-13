from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from nakormi_bot.entities.user import User
from nakormi_bot.functional.core_context import CoreContext
from nakormi_bot.functional.phrases import Phrases
from nakormi_bot.handlers.registration.states.registration import RegistrationState
from nakormi_bot.services.api.backend import Backend

router = Router(name='image_chosen')


async def complete_registration(state: FSMContext,
                                context: CoreContext,
                                phrases: Phrases,
                                bot: Bot,
                                backend: Backend):
    core_message = context.get_message()

    # TODO: Возможно, стоит перенести взаимодействие с профилем человека
    # TODO: в отдельный класс ProfileContext/UserContext

    data = await state.get_data()
    name, phone = data['name'], data['phone']
    email = data['email'] if 'email' in data else '[Не указан]'
    image = data['image'] if 'image' in data else '[Не указана]'

    await backend.users.register(User(telegram_id=core_message.telegram_id,
                                      name=name,
                                      phone=phone,
                                      email=email,
                                      avatar=image))

    await bot.edit_message_text(phrases['registration']['image']['chosen'].format(name, phone, email, image),
                                chat_id=core_message.chat_id,
                                message_id=core_message.message_id)

    await state.set_state(None)
    await state.update_data(registered=True)


@router.message(RegistrationState.waiting_for_image,
                F.photo)
async def image_chosen_handler(message: Message,
                               state: FSMContext,
                               context: CoreContext,
                               phrases: Phrases,
                               bot: Bot,
                               backend: Backend):
    image_id = message.photo[-1].file_id
    await state.update_data(image=image_id)

    await complete_registration(state, context, phrases, bot, backend)


@router.callback_query(F.data.startswith('skip_image'))
async def image_skip_handler(callback_query: CallbackQuery,
                             state: FSMContext,
                             context: CoreContext,
                             phrases: Phrases,
                             bot: Bot,
                             backend: Backend):
    await complete_registration(state, context, phrases, bot, backend)


@router.message(RegistrationState.waiting_for_image)
async def image_chosen_invalid_handler(message: Message,
                                       state: FSMContext,
                                       context: CoreContext,
                                       phrases: Phrases,
                                       bot: Bot):
    core_message = context.get_message()

    await bot.edit_message_text(phrases['registration']['image']['invalid'],
                                chat_id=core_message.chat_id,
                                message_id=core_message.message_id)
