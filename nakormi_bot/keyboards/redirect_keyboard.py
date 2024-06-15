from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from functional.phrases import Phrases


def make_redirect_keyboard(destination_callback: str, text: str) -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()

    builder.row(InlineKeyboardButton(text=text,
                                     callback_data=destination_callback))
    return builder
