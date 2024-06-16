from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from filters.regex_match_filter import RegexMatchFilter
from functional.core_context import CoreContext
from functional.phrases import Phrases
from functional.representate_point import represent_points
from keyboards.admin_keyboard import admin_user_is_admin

from handlers.admin.states.admin import AddUserAdminState
from keyboards.redirect_keyboard import make_redirect_keyboard
from services.api.backend import Backend

router = Router(name='admin_user')


@router.callback_query(F.data.startswith('admin_add_volunteer'))
async def admin_add_volunteer(callback_query: CallbackQuery,
                        state: FSMContext,
                        context: CoreContext,
                        phrases: Phrases,
                        bot: Bot):
    core_message = context.get_message()

    await bot.edit_message_text(phrases['admin']['user']['text'],
                                chat_id=core_message.chat_id,
                                message_id=core_message.message_id,
                                parse_mode='HTML')
    await state.set_state(AddUserAdminState.waiting_for_id)


@router.message(AddUserAdminState.waiting_for_id,
                RegexMatchFilter(r'^[\d]+$'))
async def id_hander(message: Message,
                    state: FSMContext,
                    context: CoreContext,
                    phrases: Phrases,
                    bot: Bot):
    core_message = context.get_message()
    await state.update_data(admin_user_tg_id=int(message.text))

    reply_markup = admin_user_is_admin()

    await bot.edit_message_text(phrases['admin']['user']['is_admin'],
                                chat_id=core_message.chat_id,
                                message_id=core_message.message_id,
                                reply_markup=reply_markup.as_markup(),
                                parse_mode='HTML')

    await state.set_state(AddUserAdminState.waiting_for_is_admin)


@router.callback_query(AddUserAdminState.waiting_for_is_admin, F.data.startswith('admin_user_role'))
async def admin_user_is_admin_view(callback_query: CallbackQuery,
                              state: FSMContext,
                              context: CoreContext,
                              phrases: Phrases,
                              bot: Bot,
                              backend: Backend):
    core_message = context.get_message()
    data = await state.get_data()
    is_admin = True if callback_query.data == 'admin_user_role_admin' else False

    res = await backend.users.add_user(from_user=core_message.telegram_id,
                                 tg_id=data['admin_user_tg_id'],
                                 is_admin=is_admin)

    text = phrases['admin']['user']['end'] if res else phrases['admin']['user']['end_invalid']

    reply_markup = make_redirect_keyboard(destination_callback='menu',
                                          text=phrases['edit_profile']['back'])

    await state.set_state(None)
    await bot.edit_message_text(text,
                                chat_id=core_message.chat_id,
                                message_id=core_message.message_id,
                                reply_markup=reply_markup.as_markup(),
                                parse_mode='HTML')


@router.message(AddUserAdminState.waiting_for_id)
async def invalid_id_handler(message: Message,
                             state: FSMContext,
                             context: CoreContext,
                             phrases: Phrases,
                             bot: Bot):
    core_message = context.get_message()
    await bot.edit_message_text(phrases['admin']['user']['invalid'],
                                chat_id=core_message.chat_id,
                                message_id=core_message.message_id,
                                parse_mode='HTML')