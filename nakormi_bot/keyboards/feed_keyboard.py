from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def is_done_keyboard() -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()

    builder.row(InlineKeyboardButton(text='Добавить ещё',
                                     callback_data='again_share'))

    builder.row(InlineKeyboardButton(text='Готово',
                                     callback_data='stop_share'))
    return builder


def is_done_photos_keyboard() -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()

    builder.row(InlineKeyboardButton(text='Остановить',
                                     callback_data='stop_photo_feed'))

    return builder