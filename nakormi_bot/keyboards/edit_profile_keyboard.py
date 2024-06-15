from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from functional.phrases import Phrases


def make_edit_profile_keyboard(phrases: Phrases) -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()

    for option in phrases['edit_profile']['options']:
        builder.row(InlineKeyboardButton(text=option['button_text'],
                                         callback_data=f'edit_{option["type"]}'))

    builder.row(InlineKeyboardButton(text=phrases['edit_profile']['back'],
                                     callback_data='menu'))

    return builder
