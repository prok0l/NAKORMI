from aiogram.fsm.state import State, StatesGroup


class ShareState(StatesGroup):
    waiting_for_tg_id = State()
    waiting_for_tags = State()
    waiting_for_volume = State()
