from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from entities.point import Point
from filters.regex_match_filter import RegexMatchFilter
from functional.core_context import CoreContext
from functional.phrases import Phrases
from handlers.registration.states.registration import RegistrationState
from keyboards.redirect_keyboard import make_redirect_keyboard
from handlers.admin.states.admin import PointAdminState

from services.api.backend import Backend

router = Router(name='admin_point_photo')


@router.message(PointAdminState.waiting_for_photo,
                F.photo)
async def waiting_for_phone(message: Message,
                            state: FSMContext,
                            context: CoreContext,
                            phrases: Phrases,
                            bot: Bot,
                            backend: Backend):
    core_message = context.get_message()

    data = await state.get_data()

    obj = message.photo[-1]
    file = await message.bot.download(file=obj.file_id, destination="images\\file.png")
    with open("images\\file.png", "rb") as f:
        obj = Point(name=data.get('admin_point_name'),
                    address=data.get('admin_point_address'),
                    lat=data.get('admin_point_lat'),
                    lon=data.get('admin_point_lon'),
                    district=data.get('admin_point_district'),
                    phone=data.get('admin_point_phone'),
                    info=data.get('admin_point_info'),
                    photo=None,
                    id=None,
                    is_active=True)
        await backend.points.create_point(from_user=core_message.telegram_id,
                                          point_obj=obj,
                                          file={'photo': f})

    await state.set_state(None)

    reply_markup = make_redirect_keyboard(destination_callback='menu',
                                          text=phrases['edit_profile']['back'])

    await bot.edit_message_text(phrases['admin']['point_create']['end'],
                                chat_id=core_message.chat_id,
                                message_id=core_message.message_id,
                                reply_markup=reply_markup.as_markup(),
                                parse_mode='HTML')


@router.callback_query(PointAdminState.waiting_for_photo, F.data.startswith('admin_point_skip_photo'))
async def image_skip_handler(callback_query: CallbackQuery,
                             state: FSMContext,
                             context: CoreContext,
                             phrases: Phrases,
                             bot: Bot,
                             backend: Backend):
    core_message = context.get_message()
    data = await state.get_data()

    obj = Point(name=data.get('admin_point_name'),
                address=data.get('admin_point_address'),
                lat=data.get('admin_point_lat'),
                lon=data.get('admin_point_lon'),
                district=data.get('admin_point_district'),
                phone=data.get('admin_point_phone'),
                info=data.get('admin_point_info'),
                photo=None,
                id=None,
                is_active=True)

    await backend.points.create_point(from_user=core_message.telegram_id,
                                      point_obj=obj,
                                      file=None)

    await state.set_state(None)

    reply_markup = make_redirect_keyboard(destination_callback='menu',
                                          text=phrases['edit_profile']['back'])

    await bot.edit_message_text(phrases['admin']['point_create']['end'],
                                chat_id=core_message.chat_id,
                                message_id=core_message.message_id,
                                reply_markup=reply_markup.as_markup(),
                                parse_mode='HTML')