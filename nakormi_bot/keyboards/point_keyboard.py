from aiogram.types import InlineKeyboardButton, WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder

from services.api.backend import Backend


def point_keyboard(backend: Backend) -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()

    builder.row(InlineKeyboardButton(text='Вернуться назад',
                                     callback_data='menu'))

    # builder.row(InlineKeyboardButton(text='Открыть карту',
    #                                  web_app=WebAppInfo(url=backend.points.map)))

    builder.row(InlineKeyboardButton(text='Открыть карту',
                                     callback_data='map'))

    builder.row(InlineKeyboardButton(text='Забрать с точки',
                                     callback_data='take_feed'))

    return builder


def is_done_keyboard() -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()

    builder.row(InlineKeyboardButton(text='Добавить ещё',
                                     callback_data='again_point'))

    builder.row(InlineKeyboardButton(text='Готово',
                                     callback_data='stop_point'))
    return builder