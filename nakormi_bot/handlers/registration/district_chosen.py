from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from functional.core_context import CoreContext
from functional.phrases import Phrases
from handlers.registration.states.registration import RegistrationState
from keyboards.skip_keyboard import make_skip_keyboard

router = Router(name='district_chosen')


@router.message(RegistrationState.waiting_for_district,
                F.text.len() >= 2,
                F.text.len() <= 10)
async def district_chosen_handler(message: Message,
                                  state: FSMContext,
                                  context: CoreContext,
                                  phrases: Phrases,
                                  bot: Bot):
    core_message = context.get_message()

    district = message.text
    data = await state.get_data()
    if district not in data['districts']:
        await district_chosen_handler(message, state, context, phrases, bot)
        return
    await state.update_data(district=district)

    reply_markup = make_skip_keyboard('skip_email', phrases)

    await bot.edit_message_text(phrases['registration']['district']['chosen'],
                                chat_id=core_message.chat_id,
                                message_id=core_message.message_id,
                                reply_markup=reply_markup.as_markup(),
                                parse_mode='HTML')

    await state.set_state(RegistrationState.waiting_for_email)


@router.message(RegistrationState.waiting_for_district)
async def distict_chosen_invalid_handler(message: Message,
                                         state: FSMContext,
                                         context: CoreContext,
                                         phrases: Phrases,
                                         bot: Bot):
    core_message = context.get_message()

    data = await state.get_data()
    msg_text = phrases['registration']['district']['invalid'] + ", ".join(data['districts'])
    await bot.edit_message_text(msg_text,
                                chat_id=core_message.chat_id,
                                message_id=core_message.message_id,
                                parse_mode='HTML')
