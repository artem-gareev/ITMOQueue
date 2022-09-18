from aiogram.dispatcher.filters.state import State, StatesGroup


class UserStates(StatesGroup):
    MAIN_MENU = State()
    SELECT_QUEUE = State()
    MANAGE_QUEUE = State()
