from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def main_menu_keyboard() -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()

    builder.row(InlineKeyboardButton(text='Редактировать профиль',
                                     callback_data='edit_profile'))

    builder.row(InlineKeyboardButton(text='Точки',
                                     callback_data='point'))

    builder.row(InlineKeyboardButton(text='Поделиться кормом',
                                     callback_data='share_feed'))

    builder.row(InlineKeyboardButton(text='Отчет о реализации',
                                     callback_data='report_feed'))

    return builder
