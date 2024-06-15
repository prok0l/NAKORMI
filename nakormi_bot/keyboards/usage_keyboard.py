from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton


def is_done_keyboard() -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()

    builder.row(InlineKeyboardButton(text='Добавить ещё',
                                     callback_data='again_usage'))

    builder.row(InlineKeyboardButton(text='Готово',
                                     callback_data='stop_usage'))

    return builder


def is_done_photos_keyboard() -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()

    builder.row(InlineKeyboardButton(text='Остановить',
                                     callback_data='stop_photo_usage'))

    return builder