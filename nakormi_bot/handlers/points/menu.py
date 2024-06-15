import asyncio
from string import digits
from typing import List

from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from entities.point import Point
from functional.representate_point import represent_points
from functional.representate_user import represent_user
from keyboards.main_menu_keyboard import main_menu_keyboard
from functional.core_context import CoreContext
from functional.phrases import Phrases

from keyboards.point_keyboard import point_keyboard, is_done_keyboard, is_done_photos_keyboard
from services.api.backend import Backend
from handlers.points.state.point import PointState

router = Router(name='point')


@router.callback_query(F.data.startswith('point'))
async def point_menu_handler(callback_query: CallbackQuery,
                             state: FSMContext,
                             context: CoreContext,
                             phrases: Phrases,
                             bot: Bot,
                             backend: Backend):
    core_message = context.get_message()

    keyboard = point_keyboard(backend)
    await bot.edit_message_text(phrases['point']['menu'],
                                chat_id=core_message.chat_id,
                                message_id=core_message.message_id,
                                reply_markup=keyboard.as_markup(),
                                parse_mode='HTML')
    await state.set_state(PointState.waiting_for_action)


@router.callback_query(F.data.startswith('map'))
async def view_map_handler(callback_query: CallbackQuery,
                           state: FSMContext,
                           context: CoreContext,
                           phrases: Phrases,
                           bot: Bot,
                           backend: Backend):
    core_message = context.get_message()

    keyboard = point_keyboard(backend)
    await bot.edit_message_text(phrases['point']['map'].format(url=backend.points.map),
                                chat_id=core_message.chat_id,
                                message_id=core_message.message_id,
                                reply_markup=keyboard.as_markup(),
                                parse_mode='HTML')


@router.callback_query(F.data.startswith('menu'))
async def to_main_handler(callback_query: CallbackQuery,
                          state: FSMContext,
                          context: CoreContext,
                          phrases: Phrases,
                          bot: Bot,
                          backend: Backend):
    core_message = context.get_message()

    inventory = await backend.users.inventory(core_message.telegram_id)
    user = await backend.users.get(core_message.telegram_id)
    analytics = await backend.users.analytics(core_message.telegram_id)
    keyboard = main_menu_keyboard(user)
    await bot.edit_message_text(represent_user(user=user, inventory=inventory, phrase=phrases, analytics=analytics),
                                chat_id=core_message.chat_id,
                                message_id=core_message.message_id,
                                reply_markup=keyboard.as_markup(),
                                parse_mode='HTML')
    return


@router.callback_query(F.data.startswith('take_feed'))
async def take_feed_handler(callback_query: CallbackQuery,
                            state: FSMContext,
                            context: CoreContext,
                            phrases: Phrases,
                            bot: Bot,
                            backend: Backend):
    core_message = context.get_message()
    points = [Point(**item) for item in await backend.points.get_points(user_id=core_message.telegram_id)]
    await state.update_data(points=points)

    msg_text = phrases['point']['points_list'] + represent_points(points=points, phrase=phrases)
    await bot.edit_message_text(msg_text,
                                chat_id=core_message.chat_id,
                                message_id=core_message.message_id,
                                parse_mode='HTML')
    await state.set_state(PointState.waiting_for_point_num)
    await state.update_data(tags=[])
    await state.update_data(content=[])
    await state.update_data(tags_values=[])
    await state.update_data(file_ids=[])
    await state.update_data(point=None)



@router.message(PointState.waiting_for_point_num)
async def select_point_handler(message: Message,
                               state: FSMContext,
                               context: CoreContext,
                               phrases: Phrases,
                               bot: Bot,
                               backend: Backend):
    core_message = context.get_message()

    num = message.text
    data = await state.get_data()
    if not set(num) <= set(digits) or not (1 <= (num := int(num)) <= len(data.get('points'))):
        msg_text = (phrases['point']['select']['invalid'] + phrases['point']['points_list']
                    + represent_points(points=data.get('points'), phrase=phrases))
        await bot.edit_message_text(msg_text,
                                    chat_id=core_message.chat_id,
                                    message_id=core_message.message_id,
                                    parse_mode='HTML')
        return

    point = data['points'][num - 1]
    await state.update_data(point=point)

    tags = await backend.feed.tags(user_id=core_message.telegram_id, level=1)

    await state.update_data(tag_db=tags)
    keyboard = InlineKeyboardBuilder()
    for item in tags:
        keyboard.row(InlineKeyboardButton(text=item.name,
                                          callback_data=str(item.id)))
    await bot.edit_message_text(phrases['point']['tags'],
                                chat_id=core_message.chat_id,
                                message_id=core_message.message_id,
                                reply_markup=keyboard.as_markup(),
                                parse_mode='HTML')

    await state.set_state(PointState.waiting_for_tags)
    await state.update_data(tags=[])
    await state.update_data(tags_values=[])


@router.callback_query(PointState.waiting_for_tags)
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
        await state.set_state(PointState.waiting_for_volume)
        await bot.edit_message_text(phrases['point']['number']['text'],
                                    chat_id=core_message.chat_id,
                                    message_id=core_message.message_id,
                                    parse_mode='HTML')
        return

    keyboard = InlineKeyboardBuilder()
    for item in tags:
        keyboard.row(InlineKeyboardButton(text=item.name,
                                          callback_data=str(item.id)))

    await bot.edit_message_reply_markup(chat_id=core_message.chat_id,
                                        message_id=core_message.message_id,
                                        reply_markup=keyboard.as_markup())


@router.message(PointState.waiting_for_volume)
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
                                    message_id=core_message.message_id,
                                    parse_mode='HTML')
        return

    content = data.get('content', [])
    # группировка одинаковых слотов в один
    ind = -1
    for i, item in enumerate(content):
        if item['tags'] == data['tags']:
            ind = i
    if ind == -1:
        content = content + [{"tags": data['tags'], "volume": volume, "tags_values": data['tags_values']}]
        await state.update_data(content=content)
    else:
        content[ind]["volume"] += volume
        await state.update_data(content=content)

    msg_text = phrases['point']['files'] + phrases['point']['inventory']['text']

    for item in content:
        msg_text += phrases['point']['inventory']['item'].format(
            name=" ".join(item['tags_values']), volume=str(item['volume']))

    keyboard = is_done_photos_keyboard()
    await bot.edit_message_text(msg_text,
                                chat_id=core_message.chat_id,
                                message_id=core_message.message_id,
                                reply_markup=keyboard.as_markup(),
                                parse_mode='HTML')
    await state.set_state(PointState.waiting_for_photo)


@router.callback_query(F.data.startswith('stop_photo_point'))
async def point_stop_photo_handler(callback_query: CallbackQuery,
                        state: FSMContext,
                        context: CoreContext,
                        phrases: Phrases,
                        bot: Bot,
                        backend: Backend):
    core_message = context.get_message()
    data = await state.get_data()
    content = data.get('content', [])

    msg_text = phrases['point']['inventory']['text']

    for item in content:
        msg_text += phrases['point']['inventory']['item'].format(
            name=" ".join(item['tags_values']), volume=str(item['volume']))

    keyboard = is_done_keyboard()
    await bot.edit_message_text(msg_text,
                                chat_id=core_message.chat_id,
                                message_id=core_message.message_id,
                                reply_markup=keyboard.as_markup(),
                                parse_mode='HTML')
    content[-1]['photo_list'] = data['file_ids']
    await state.update_data(content=content)


@router.message(PointState.waiting_for_photo, F.photo)
async def photo_handler(message: Message,
                         state: FSMContext,
                         context: CoreContext,
                         phrases: Phrases,
                         bot: Bot,
                         backend: Backend):
    core_message = context.get_message()
    data = await state.get_data()
    file_ids = data['file_ids']
    obj = message.photo[-1]
    file = await message.bot.download(file=obj.file_id, destination="images\\file.png")
    with open("images\\file.png", "rb") as f:
        file_id = await backend.main.upload(file=f, user_id=core_message.telegram_id)
        file_ids.append(file_id[0])
    await state.update_data(file_ids=file_ids)


@router.callback_query(F.data.startswith('again_point'))
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

    msg_text = phrases['point']['tags'] + phrases['point']['inventory']['text']

    for item in data['content']:
        msg_text += phrases['point']['inventory']['item'].format(
            name=" ".join(item['tags_values']), volume=str(item['volume']))

    tags = await backend.feed.tags(user_id=core_message.telegram_id, level=1)
    await state.update_data(tag_db=tags)
    keyboard = InlineKeyboardBuilder()
    for item in tags:
        keyboard.row(InlineKeyboardButton(text=item.name,
                                          callback_data=str(item.id)))

    await state.set_state(PointState.waiting_for_tags)

    await bot.edit_message_text(msg_text,
                                chat_id=core_message.chat_id,
                                message_id=core_message.message_id,
                                reply_markup=keyboard.as_markup(),
                                parse_mode='HTML')


@router.callback_query(F.data.startswith('stop_point'))
async def stop_handler(callback_query: CallbackQuery,
                       state: FSMContext,
                       context: CoreContext,
                       phrases: Phrases,
                       bot: Bot,
                       backend: Backend):
    core_message = context.get_message()

    data = await state.get_data()
    content = data.get('content')
    to_user = core_message.telegram_id
    point = data['point'].id
    res = await backend.points.take(user_id=to_user, point_id=point, content=content)
    await state.update_data(report_id=res['id'])

    msg_text = phrases['point']['files_final'] + phrases['point']['inventory']['text']

    for item in content:
        msg_text += phrases['point']['inventory']['item'].format(
            name=" ".join(item['tags_values']), volume=str(item['volume']))

    await bot.edit_message_text(msg_text,
                                chat_id=core_message.chat_id,
                                message_id=core_message.message_id,
                                parse_mode='HTML')
    await state.set_state(PointState.waiting_for_document)


@router.message(PointState.waiting_for_document, F.photo)
async def document_handler(message: Message,
                         state: FSMContext,
                         context: CoreContext,
                         phrases: Phrases,
                         bot: Bot,
                         backend: Backend):
    core_message = context.get_message()

    data = await state.get_data()

    obj = message.photo[-1]
    file = await message.bot.download(file=obj.file_id, destination="images\\file.png")
    with open("images\\file.png", "rb") as f:
        file_id = await backend.feed.report_photo(user_id=core_message.telegram_id,
                                                  file=f,
                                                  report_id=data['report_id'])

    await state.set_state(None)
    await to_main_handler(callback_query=None, state=state,
                          context=context, phrases=phrases, bot=bot, backend=backend)
