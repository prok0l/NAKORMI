from aiogram.fsm.state import State, StatesGroup


class PointAdminState(StatesGroup):
    waiting_for_name = State()
    waiting_for_address = State()
    waiting_for_coords = State()
    waiting_for_photo = State()
    waiting_for_phone = State()
    waiting_for_info = State()
    waiting_for_district = State()


class DelPointAdminState(StatesGroup):
    waiting_for_num = State()