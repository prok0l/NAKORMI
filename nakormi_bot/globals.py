from aiogram import Bot, Dispatcher
from aiogram.methods import DeleteWebhook

from aiogram.fsm.storage.memory import MemoryStorage

from middlewares.throttling import ThrottlingMiddleware


async def run_app(bot_token: str):
    bot = Bot(token=bot_token)
    storage = MemoryStorage()

    # DI Dependencies
    dp = Dispatcher(storage=storage)

    dp.message.middleware(ThrottlingMiddleware(0.5))

    # dp.include_routers()

    # TODO: Uncomment due Release version
    # await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

