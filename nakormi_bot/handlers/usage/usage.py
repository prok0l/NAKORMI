from string import digits

from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from functional.core_context import CoreContext
from functional.phrases import Phrases
from handlers.points.menu import to_main_handler
from handlers.usage.state.usage import UsageState
from services.api.backend import Backend
from keyboards.usage_keyboard import is_done_keyboard, is_done_photos_keyboard

router = Router(name='usage')


@router.callback_query(F.data.startswith('usage_start'))
async def usage_handler(callback_query: CallbackQuery,
                        state: FSMContext,
                        context: CoreContext,
                        phrases: Phrases,
                        bot: Bot,
                        backend: Backend):
    core_message = context.get_message()

    inventory = await backend.users.inventory(user_id=core_message.telegram_id)
    await state.update_data(tags=[])
    await state.update_data(content=[])
    await state.update_data(tags_values=[])
    await state.update_data(file_ids=[])
    await state.update_data(inventory=inventory)
    await state.update_data(district_id=None)
    core_message = context.get_message()

    districts = await backend.main.get_districts(user_id=core_message.telegram_id)
    msg_text = phrases['usage']['district']['enter'] + ', '.join([x['name'] for x in districts])

    await state.update_data(districts=districts)
    await bot.edit_message_text(msg_text,
                                chat_id=core_message.chat_id,
                                message_id=core_message.message_id,
                                parse_mode='HTML')
    await state.set_state(UsageState.waiting_for_district)


@router.message(UsageState.waiting_for_district)
async def district_handler(message: Message,
                           state: FSMContext,
                           context: CoreContext,
                           phrases: Phrases,
                           bot: Bot,
                           backend: Backend):
    core_message = context.get_message()

    data = await state.get_data()

    text = message.text
    if text not in [x['name'] for x in data.get('districts')]:
        msg_text = (phrases['usage']['district']['invalid'] + phrases['usage']['district']['enter'] +
                    ', '.join([x['name'] for x in data.get('districts', [])]))

        await bot.edit_message_text(msg_text,
                                    chat_id=core_message.chat_id,
                                    message_id=core_message.message_id,
                                    parse_mode='HTML')
        return
    district = [x for x in data.get('districts') if x['name'] == text][0]
    await state.update_data(district_id=district['id'])

    tags = await backend.feed.tags(user_id=core_message.telegram_id, level=1)

    await state.update_data(tag_db=tags)
    keyboard = InlineKeyboardBuilder()
    for item in tags:
        keyboard.row(InlineKeyboardButton(text=item.name,
                                          callback_data=str(item.id)))

    msg_text = phrases['usage']['tags']
    await bot.edit_message_text(msg_text,
                                chat_id=core_message.chat_id,
                                message_id=core_message.message_id,
                                reply_markup=keyboard.as_markup(),
                                parse_mode='HTML')
    await state.set_state(UsageState.waiting_for_tags)
    await state.update_data(tags=[])
    await state.update_data(tags_values=[])


@router.callback_query(UsageState.waiting_for_tags)
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
        await state.set_state(UsageState.waiting_for_volume)
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


@router.message(UsageState.waiting_for_volume)
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
    else:
        content[ind]["volume"] += volume

    content_filtered = list()

    inventory = data['inventory']
    for i, item in enumerate(content):
        if any([True if inv_obj.volume >= item['volume'] and inv_obj.tags == item['tags_values'] else False
                for inv_obj in inventory]):
            content_filtered.append(item)

    msg_text = phrases['point']['files']
    if len(content_filtered) != len(content):
        msg_text += phrases['share']['inventory']['invalid']
        if content:
            msg_text += phrases['point']['inventory']['text']
            for item in content_filtered:
                msg_text += phrases['point']['inventory']['item'].format(
                    name=" ".join(item['tags_values']), volume=str(item['volume']))

        keyboard = is_done_keyboard()
        await bot.edit_message_text(msg_text,
                                    chat_id=core_message.chat_id,
                                    message_id=core_message.message_id,
                                    reply_markup=keyboard.as_markup(),
                                    parse_mode='HTML')
        return

    content = content_filtered
    await state.update_data(content=content)

    if content:
        msg_text += phrases['point']['inventory']['text']
        for item in content:
            msg_text += phrases['point']['inventory']['item'].format(
                name=" ".join(item['tags_values']), volume=str(item['volume']))

    keyboard = is_done_photos_keyboard()

    await bot.edit_message_text(msg_text,
                                chat_id=core_message.chat_id,
                                message_id=core_message.message_id,
                                reply_markup=keyboard.as_markup(),
                                parse_mode='HTML')
    await state.set_state(UsageState.waiting_for_photo)


@router.callback_query(F.data.startswith('stop_photo_usage'))
async def usage_stop_photo_handler(callback_query: CallbackQuery,
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

    if content:
        content[-1]['photo_list'] = data['file_ids']
        await state.update_data(content=content)


@router.message(UsageState.waiting_for_photo, F.photo)
async def photo_handler(message: Message,
                        state: FSMContext,
                        context: CoreContext,
                        phrases: Phrases,
                        bot: Bot,
                        backend: Backend):
    core_message = context.get_message()
    data = await state.get_data()
    file_ids = data.get('file_ids', [])
    obj = message.photo[-1]
    file = await message.bot.download(file=obj.file_id, destination="images\\file.png")
    with open("images\\file.png", "rb") as f:
        file_id = await backend.main.upload(file=f, user_id=core_message.telegram_id)
        file_ids.append(file_id[0])
    await state.update_data(file_ids=file_ids)


@router.callback_query(F.data.startswith('again_usage'))
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

    msg_text = (phrases['share']['tags'] + phrases['point']['inventory']['text'])

    for item in data['content']:
        msg_text += phrases['point']['inventory']['item'].format(
            name=" ".join(item['tags_values']), volume=str(item['volume']))

    tags = await backend.feed.tags(user_id=core_message.telegram_id, level=1)
    await state.update_data(tag_db=tags)
    keyboard = InlineKeyboardBuilder()
    for item in tags:
        keyboard.row(InlineKeyboardButton(text=item.name,
                                          callback_data=str(item.id)))

    await state.set_state(UsageState.waiting_for_tags)

    await bot.edit_message_text(msg_text,
                                chat_id=core_message.chat_id,
                                message_id=core_message.message_id,
                                reply_markup=keyboard.as_markup(),
                                parse_mode='HTML')


@router.callback_query(F.data.startswith('stop_usage'))
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
    district = data.get('district_id')

    status, res = await backend.users.usage_feed(content=content, from_user=from_user, district=district)

    await state.update_data(report_id=res['id'])

    msg_text = (phrases['point']['files_final'] +
                phrases['share']['tags'] + phrases['point']['inventory']['text'])

    for item in data['content']:
        msg_text += phrases['point']['inventory']['item'].format(
            name=" ".join(item['tags_values']), volume=str(item['volume']))

    await bot.edit_message_text(msg_text,
                                chat_id=core_message.chat_id,
                                message_id=core_message.message_id,
                                parse_mode='HTML')
    await state.set_state(UsageState.waiting_for_document)



@router.message(UsageState.waiting_for_document, F.photo)
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

