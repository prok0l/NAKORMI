from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from handlers import start_command
from middlewares.single_message import SingleMessageMiddleware
from middlewares.throttling import ThrottlingMiddleware

from handlers import undefined_command
from handlers.registration import name_chosen, phone_chosen, email_chosen, image_chosen, district_chosen
from handlers.edit_profile import edit_profile, edit_name, edit_email, edit_phone, edit_image
from handlers.points import menu
from handlers.share_feed import share
from handlers.usage import usage
from handlers.admin import admin_main, admin_point, admin_user, admin_stocks
from handlers.admin.create_point import (admin_point_name, admin_point_address, admin_point_coords, admin_point_phone,
                                         admin_point_info, admin_point_district, admin_point_photo)
from middlewares.language_middleware import LanguageMiddleware
from services.api.backend import Backend


async def run_app(bot_token: str, api_key: str, api_address: str):
    bot = Bot(token=bot_token)
    storage = MemoryStorage()
    backend = Backend("http://localhost:8000/api", api_key, api_address)

    # DI Dependencies
    dp = Dispatcher(storage=storage, bot=bot, backend=backend)

    dp.message.middleware(ThrottlingMiddleware(0.5))
    dp.message.middleware(LanguageMiddleware())
    dp.callback_query.middleware(LanguageMiddleware())
    dp.message.middleware(SingleMessageMiddleware())
    dp.callback_query.middleware(SingleMessageMiddleware())

    dp.include_router(start_command.router)

    # Registration
    dp.include_routers(name_chosen.router,
                       phone_chosen.router,
                       district_chosen.router,
                       email_chosen.router,
                       image_chosen.router,
                       menu.router,
                       share.router,
                       usage.router,
                       edit_profile.router,
                       edit_name.router,
                       edit_email.router,
                       edit_phone.router,
                       edit_image.router,
                       admin_main.router,
                       admin_point.router,
                       admin_point_name.router,
                       admin_point_address.router,
                       admin_point_coords.router,
                       admin_point_phone.router,
                       admin_point_info.router,
                       admin_point_district.router,
                       admin_point_photo.router,
                       admin_user.router,
                       admin_stocks.router
                       )

    dp.include_router(undefined_command.router)

    # TODO: Uncomment due Release version
    # await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)
