from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from handlers import start_command
from middlewares.single_message import SingleMessageMiddleware
from middlewares.throttling import ThrottlingMiddleware

from nakormi_bot.handlers import undefined_command
from nakormi_bot.handlers.registration import name_chosen, phone_chosen, email_chosen, image_chosen
from nakormi_bot.middlewares.language_middleware import LanguageMiddleware
from nakormi_bot.services.api.backend import Backend


async def run_app(bot_token: str, api_key: str):
    bot = Bot(token=bot_token)
    storage = MemoryStorage()
    backend = Backend('http://localhost:8000/api/', api_key)

    # DI Dependencies
    dp = Dispatcher(storage=storage, bot=bot)

    dp.message.middleware(ThrottlingMiddleware(0.5))
    dp.message.middleware(LanguageMiddleware())
    dp.callback_query.middleware(LanguageMiddleware())
    dp.message.middleware(SingleMessageMiddleware())
    dp.callback_query.middleware(SingleMessageMiddleware())

    dp.include_router(start_command.router)

    # Registration
    dp.include_routers(name_chosen.router,
                       phone_chosen.router,
                       email_chosen.router,
                       image_chosen.router)

    dp.include_router(undefined_command.router)

    # TODO: Uncomment due Release version
    # await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)
