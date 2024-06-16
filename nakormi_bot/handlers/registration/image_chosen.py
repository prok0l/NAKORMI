from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from entities.user import User
from functional.core_context import CoreContext
from functional.phrases import Phrases
from functional.representate_user import represent_user
from handlers.registration.states.registration import RegistrationState
from services.api.backend import Backend
from keyboards.main_menu_keyboard import main_menu_keyboard

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
    name, phone, district = data['name'], data['phone'], data['district']
    email = data['email'] if 'email' in data else None

    await backend.users.register(User(tg_id=core_message.telegram_id,
                                      name=name,
                                      phone=phone,
                                      email=email,
                                      image=None,
                                      district=district))

    user = await backend.users.get(user_id=core_message.telegram_id)
    analytics = await backend.users.analytics(from_user=core_message.telegram_id)
    inventory = await backend.users.inventory(user_id=core_message.telegram_id)
    keyboard = main_menu_keyboard(user)
    msg_text = phrases['registration']['image']['chosen'] + represent_user(user=user,
                                                                           inventory=inventory,
                                                                           phrase=phrases,
                                                                           analytics=analytics)
    await bot.edit_message_text(msg_text,
                                chat_id=core_message.chat_id,
                                message_id=core_message.message_id,
                                reply_markup=keyboard.as_markup(),
                                parse_mode='HTML'
                                )

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
    core_message = context.get_message()

    obj = message.photo[-1]
    file = await message.bot.download(file=obj.file_id, destination="images\\avatar.png")
    with open("images\\avatar.png", "rb") as f:
        file_id = await backend.users.upload_avatar(file=f, user_id=core_message.telegram_id)

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
                                message_id=core_message.message_id,
                                parse_mode='HTML')
