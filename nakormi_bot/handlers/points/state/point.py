from aiogram.fsm.state import State, StatesGroup


class PointState(StatesGroup):
    waiting_for_action = State()
    waiting_for_point_num = State()
    waiting_for_tags = State()
    waiting_for_volume = State()
    waiting_for_photo = State()
    waiting_for_document = State()
