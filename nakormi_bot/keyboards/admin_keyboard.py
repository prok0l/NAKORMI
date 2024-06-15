from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def admin_keyboard() -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()

    builder.row(InlineKeyboardButton(text='Создание/удаление точки',
                                     callback_data='admin_edit_point'))

    builder.row(InlineKeyboardButton(text='Добавить волонтера',
                                     callback_data='admin_add_volunteer'))

    builder.row(InlineKeyboardButton(text='Складские запасы',
                                     callback_data='admin_stocks'))

    return builder


def admin_point_keyboard() -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()

    builder.row(InlineKeyboardButton(text='Создать точку',
                                     callback_data='admin_create_point'))

    builder.row(InlineKeyboardButton(text="Удалить точку",
                                     callback_data='admin_del_point'))

    return builder


def admin_point_photo() -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()

    builder.row(InlineKeyboardButton(text='Не прикреплять фотографию',
                                     callback_data='admin_point_skip_photo'))

    return builder