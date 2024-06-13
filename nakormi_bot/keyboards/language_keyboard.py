from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from nakormi_bot.functional.phrases import Phrases


def make_language_keyboard() -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()

    builder.row(InlineKeyboardButton(text='🇷🇺 Русский',
                                     callback_data='language_ru'))

    builder.row(InlineKeyboardButton(text='🇰🇿 Қазақша',
                                     callback_data='language_kz'))

    builder.row(InlineKeyboardButton(text='🇬🇧 English',
                                     callback_data='language_en'))

    builder.row(InlineKeyboardButton(text='🇫🇷 Français',
                                     callback_data='language_fr'))

    return builder
