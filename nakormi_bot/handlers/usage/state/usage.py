from aiogram.fsm.state import State, StatesGroup


class UsageState(StatesGroup):
    waiting_for_district = State()
    waiting_for_tags = State()
    waiting_for_volume = State()
    waiting_for_photo = State()
    waiting_for_document = State()