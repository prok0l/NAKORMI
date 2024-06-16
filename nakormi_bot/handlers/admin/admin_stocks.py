from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from setuptools.package_index import user_agent

from filters.regex_match_filter import RegexMatchFilter
from functional.core_context import CoreContext
from functional.phrases import Phrases
from handlers.admin.states.admin import StocksAdminState
from keyboards.admin_keyboard import admin_keyboard
from keyboards.redirect_keyboard import make_redirect_keyboard
from services.api.backend import Backend

router = Router(name='admin_stocks')


@router.callback_query(F.data.startswith('admin_stocks'))
async def stocks_handler(callback_query: CallbackQuery,
                         state: FSMContext,
                         context: CoreContext,
                         phrases: Phrases,
                         bot: Bot,
                         backend: Backend):
    core_message = context.get_message()

    districts = await backend.main.get_districts(user_id=core_message.telegram_id)

    await state.update_data(districts=districts)
    await state.set_state(StocksAdminState.waiting_for_district)

    msg_text = (phrases['admin']['stocks']['text'] +
                phrases['admin']['point_create']['district']['second']) + ", ".join(x['name'] for x in districts)

    await bot.edit_message_text(msg_text,
                                chat_id=core_message.chat_id,
                                message_id=core_message.message_id,
                                parse_mode='HTML')


@router.message(StocksAdminState.waiting_for_district,
                F.text.len() >= 2,
                F.text.len() <= 5)
async def admin_point_district(message: Message,
                               state: FSMContext,
                               context: CoreContext,
                               phrases: Phrases,
                               bot: Bot,
                               backend: Backend
                               ):
    core_message = context.get_message()
    data = await state.get_data()

    if message.text not in [x['name'] for x in data['districts']]:
        await bot.edit_message_text(phrases['admin']['point_create']['district']['invalid'],
                                    chat_id=core_message.chat_id,
                                    message_id=core_message.message_id,
                                    parse_mode='HTML')
        return

    district = message.text
    stocks_values = await backend.users.get_district_analytics(from_user=core_message.telegram_id,
                                                                district=district)
    msg_text = phrases['admin']['stocks']['end']
    for item in stocks_values:
        msg_text += phrases["main"]["inventory"]["line"].format(tags_line=" ".join(item['tags']),
                                                                volume=item['volume'])

    reply_markup = make_redirect_keyboard(destination_callback='menu',
                                          text=phrases['edit_profile']['back'])

    await state.set_state(None)

    await bot.edit_message_text(msg_text,
                                chat_id=core_message.chat_id,
                                message_id=core_message.message_id,
                                reply_markup=reply_markup.as_markup(),
                                parse_mode='HTML')



@router.message(StocksAdminState.waiting_for_district)
async def invalid_district(message: Message,
                           state: FSMContext,
                           context: CoreContext,
                           phrases: Phrases,
                           bot: Bot,
                           backend: Backend):
    core_message = context.get_message()

    msg = phrases['admin']['stocks']['district']['invalid']

    await bot.edit_message_text(msg,
                                chat_id=core_message.chat_id,
                                message_id=core_message.message_id,
                                parse_mode='HTML')