from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command

router = Router(name='start_command')


@router.message(F.text, Command('start'))
async def start_command_handler(message: Message):
    await message.answer('Привет!')
