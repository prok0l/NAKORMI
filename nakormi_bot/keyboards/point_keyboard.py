from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def point_keyboard() -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()

    builder.row(InlineKeyboardButton(text='Вернуться назад',
                                     callback_data='menu'))

    builder.row(InlineKeyboardButton(text='Открыть карту',
                                     callback_data='map'))

    builder.row(InlineKeyboardButton(text='Забрать с точки',
                                     callback_data='take_feed'))

    return builder


def is_done_keyboard() -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()

    builder.row(InlineKeyboardButton(text='Добавить ещё',
                                     callback_data='again'))

    builder.row(InlineKeyboardButton(text='Готово',
                                     callback_data='stop'))
    return builder