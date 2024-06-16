from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from entities.point import Point
from filters.regex_match_filter import RegexMatchFilter
from functional.core_context import CoreContext
from functional.phrases import Phrases
from functional.representate_point import represent_points
from handlers.registration.states.registration import RegistrationState
from keyboards.admin_keyboard import admin_point_keyboard
from handlers.admin.states.admin import DelPointAdminState, PointAdminState
from keyboards.redirect_keyboard import make_redirect_keyboard

from services.api.backend import Backend

router = Router(name='admin_point')


@router.callback_query(F.data.startswith('admin_edit_point'))
async def edit_profile_handler(callback_query: CallbackQuery,
                               state: FSMContext,
                               context: CoreContext,
                               phrases: Phrases,
                               bot: Bot):
    core_message = context.get_message()

    keyboard = admin_point_keyboard()

    await bot.edit_message_text(phrases['admin']['point'],
                                chat_id=core_message.chat_id,
                                message_id=core_message.message_id,
                                reply_markup=keyboard.as_markup(),
                                parse_mode='HTML')


@router.callback_query(F.data.startswith('admin_create_point'))
async def create_point_handler(callback_query: CallbackQuery,
                               state: FSMContext,
                               context: CoreContext,
                               phrases: Phrases,
                               bot: Bot):
    core_message = context.get_message()

    await bot.edit_message_text(phrases['admin']['point_create']['name']['text'],
                                chat_id=core_message.chat_id,
                                message_id=core_message.message_id,
                                parse_mode='HTML')
    await state.set_state(PointAdminState.waiting_for_name)


@router.callback_query(F.data.startswith('admin_del_point'))
async def delete_point_handler(callback_query: CallbackQuery,
                               state: FSMContext,
                               context: CoreContext,
                               phrases: Phrases,
                               bot: Bot,
                               backend: Backend):
    core_message = context.get_message()

    points = await backend.points.get_points(user_id=core_message.telegram_id)
    msg = (phrases['admin']['point_delete']['text'] +
           represent_points(points=[Point(**x)
                                    for x in await backend.points.get_points(
                   user_id=core_message.telegram_id)], phrase=phrases))
    await bot.edit_message_text(msg,
                                chat_id=core_message.chat_id,
                                message_id=core_message.message_id,
                                parse_mode='HTML')

    await state.update_data(points=points)
    await state.set_state(DelPointAdminState.waiting_for_num)


@router.message(DelPointAdminState.waiting_for_num,
                RegexMatchFilter(r'^[\d]+$'))
async def del_num_handler(message: Message,
                    state: FSMContext,
                    context: CoreContext,
                    phrases: Phrases,
                    bot: Bot,
                    backend: Backend
                    ):
    core_message = context.get_message()
    data = await state.get_data()

    if int(message.text) >= len(data['points']):
        await invalid_del_num_validator(message, state, context, phrases, bot, backend)

    ind = int(message.text) - 1

    point = data['points'][ind]
    point['is_active'] = False
    await backend.points.update_point(from_user=core_message.telegram_id, data=point)

    reply_markup = make_redirect_keyboard(destination_callback='menu',
                                          text=phrases['edit_profile']['back'])

    await state.set_state(None)
    await bot.edit_message_text(phrases['admin']['point_delete']['end'],
                                chat_id=core_message.chat_id,
                                message_id=core_message.message_id,
                                reply_markup=reply_markup.as_markup(),
                                parse_mode='HTML')


@router.message(DelPointAdminState.waiting_for_num)
async def invalid_del_num_validator(message: Message,
                    state: FSMContext,
                    context: CoreContext,
                    phrases: Phrases,
                    bot: Bot,
                    backend: Backend
                    ):
    core_message = context.get_message()
    msg = (phrases['admin']['point_delete']['invalid'] + phrases['admin']['point_delete']['text'] +
           represent_points(points=[Point(**x)
                                    for x in await backend.points.get_points(
                   user_id=core_message.telegram_id)], phrase=phrases))
    await bot.edit_message_text(msg,
                                chat_id=core_message.chat_id,
                                message_id=core_message.message_id,
                                parse_mode='HTML')