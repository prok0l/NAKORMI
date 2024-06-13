from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from nakormi_bot.functional.phrases import Phrases


def make_skip_keyboard(on_click: str, phrases: Phrases) -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()

    builder.row(InlineKeyboardButton(text=phrases['skip_button'],
                                     callback_data=on_click))
    return builder
