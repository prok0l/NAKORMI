from string import digits

from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from functional.core_context import CoreContext
from functional.phrases import Phrases
from handlers.points.menu import to_main_handler
from keyboards.feed_keyboard import is_done_keyboard
from services.api.backend import Backend

from handlers.share_feed.state.share import ShareState

router = Router(name='share')


@router.callback_query(F.data.startswith('share_feed'))
async def share_feed_handler(callback_query: CallbackQuery,
                             state: FSMContext,
                             context: CoreContext,
                             phrases: Phrases,
                             bot: Bot,
                             backend: Backend):
    core_message = context.get_message()

    await bot.edit_message_text(phrases['share']['tg_id']['start'],
                                chat_id=core_message.chat_id,
                                message_id=core_message.message_id)
    await state.set_state(ShareState.waiting_for_tg_id)
    inventory = await backend.users.inventory(user_id=core_message.telegram_id)

    await state.update_data(inventory=inventory)
    await state.update_data(tags=[])
    await state.update_data(content=[])
    await state.update_data(tags_values=[])
    await state.update_data(point=None)


@router.message(ShareState.waiting_for_tg_id)
async def input_tg_id_handler(message: Message,
                              state: FSMContext,
                              context: CoreContext,
                              bot: Bot,
                              phrases: Phrases,
                              backend: Backend):
    core_message = context.get_message()
    id = message.text
    if not set(id) <= set(digits) or not await backend.users.check(user_id=core_message.telegram_id, searched_user=id):
        await bot.edit_message_text(phrases['share']['tg_id']['invalid'],
                                    chat_id=core_message.chat_id,
                                    message_id=core_message.message_id)
        return

    await state.update_data(to_user=int(id))
    await state.set_state(ShareState.waiting_for_tags)

    tags = await backend.feed.tags(user_id=core_message.telegram_id, level=1)

    await state.update_data(tag_db=tags)
    keyboard = InlineKeyboardBuilder()
    for item in tags:
        keyboard.row(InlineKeyboardButton(text=item.name,
                                          callback_data=str(item.id)))

    await bot.edit_message_text(phrases['share']['to_user'].format(id=id) + phrases['share']['tags'],
                                chat_id=core_message.chat_id,
                                message_id=core_message.message_id,
                                reply_markup=keyboard.as_markup())
    await state.update_data(tags=[])
    await state.update_data(tags_values=[])


@router.callback_query(ShareState.waiting_for_tags)
async def tags_handler(callback_query: CallbackQuery,
                       state: FSMContext,
                       context: CoreContext,
                       phrases: Phrases,
                       bot: Bot,
                       backend: Backend):
    core_message = context.get_message()

    data = await state.get_data()
    now_tags = data['tags'] + [int(callback_query.data)]
    now_tags_values = data['tags_values'] + [x.name for x in data['tag_db'] if x.id == int(callback_query.data)]
    await state.update_data(tags=now_tags)
    await state.update_data(tags_values=now_tags_values)

    tags = await backend.feed.tags(user_id=core_message.telegram_id,
                                   level=(len(now_tags) + 1))
    await state.update_data(tag_db=tags)

    if not tags:
        await state.set_state(ShareState.waiting_for_volume)
        await bot.edit_message_text(phrases['point']['number']['text'],
                                    chat_id=core_message.chat_id,
                                    message_id=core_message.message_id)
        return

    keyboard = InlineKeyboardBuilder()
    for item in tags:
        keyboard.row(InlineKeyboardButton(text=item.name,
                                          callback_data=str(item.id)))

    await bot.edit_message_reply_markup(chat_id=core_message.chat_id,
                                        message_id=core_message.message_id,
                                        reply_markup=keyboard.as_markup())


@router.message(ShareState.waiting_for_volume)
async def volume_handler(message: Message,
                         state: FSMContext,
                         context: CoreContext,
                         phrases: Phrases,
                         bot: Bot,
                         backend: Backend):
    core_message = context.get_message()
    volume = message.text
    data = await state.get_data()

    if not set(volume) <= set(digits) or not (1 <= (volume := int(volume))):
        msg_text = phrases['point']['number']['invalid']
        if data.get('content', []):
            msg_text += phrases['point']['inventory']['text']
            for item in data['content']:
                msg_text += phrases['point']['inventory']['item'].format(name="".join(item.tags), volume=item.volume)
        await bot.edit_message_text(msg_text,
                                    chat_id=core_message.chat_id,
                                    message_id=core_message.message_id)
        return

    content = data.get('content', [])
    # группировка одинаковых слотов в один
    ind = -1
    for i, item in enumerate(content):
        if item['tags'] == data['tags']:
            ind = i
    if ind == -1:
        content = content + [{"tags": data['tags'], "volume": volume, "tags_values": data['tags_values']}]
    else:
        content[ind]["volume"] += volume

    content_filtered = list()

    inventory = data['inventory']
    for i, item in enumerate(content):
        if any([True if inv_obj.volume >= item['volume'] and inv_obj.tags == item['tags_values'] else False
                for inv_obj in inventory]):
            content_filtered.append(item)
    msg_text = str()
    if len(content_filtered) != len(content):
        msg_text += phrases['share']['inventory']['invalid']

    content = content_filtered
    await state.update_data(content=content)
    msg_text += phrases['share']['to_user'].format(id=data['to_user'])
    if content:
        msg_text += phrases['point']['inventory']['text']

    for item in content:
        msg_text += phrases['point']['inventory']['item'].format(
            name=" ".join(item['tags_values']), volume=str(item['volume']))

    keyboard = is_done_keyboard()
    await bot.edit_message_text(msg_text,
                                chat_id=core_message.chat_id,
                                message_id=core_message.message_id,
                                reply_markup=keyboard.as_markup())


@router.callback_query(F.data.startswith('again_share'))
async def again_handler(callback_query: CallbackQuery,
                        state: FSMContext,
                        context: CoreContext,
                        phrases: Phrases,
                        bot: Bot,
                        backend: Backend):
    core_message = context.get_message()

    data = await state.get_data()
    await state.update_data(tags=[])
    await state.update_data(tags_values=[])

    msg_text = (phrases['share']['to_user'].format(id=data['to_user']) +
                phrases['share']['tags'] + phrases['point']['inventory']['text'])

    for item in data['content']:
        msg_text += phrases['point']['inventory']['item'].format(
            name=" ".join(item['tags_values']), volume=str(item['volume']))

    tags = await backend.feed.tags(user_id=core_message.telegram_id, level=1)
    await state.update_data(tag_db=tags)
    keyboard = InlineKeyboardBuilder()
    for item in tags:
        keyboard.row(InlineKeyboardButton(text=item.name,
                                          callback_data=str(item.id)))

    await state.set_state(ShareState.waiting_for_tags)

    await bot.edit_message_text(msg_text,
                                chat_id=core_message.chat_id,
                                message_id=core_message.message_id,
                                reply_markup=keyboard.as_markup())


@router.callback_query(F.data.startswith('stop_share'))
async def stop_handler(callback_query: CallbackQuery,
                       state: FSMContext,
                       context: CoreContext,
                       phrases: Phrases,
                       bot: Bot,
                       backend: Backend):
    core_message = context.get_message()

    data = await state.get_data()
    content = data.get('content')
    from_user = core_message.telegram_id
    to_user = data['to_user']

    # await backend.points.take(user_id=to_user, point_id=point, content=content)
    await state.set_state(None)
    await to_main_handler(callback_query=callback_query, state=state,
                          context=context, phrases=phrases, bot=bot, backend=backend)
