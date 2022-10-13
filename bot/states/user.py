from aiogram.dispatcher.filters.state import State, StatesGroup


class UserStates(StatesGroup):
    MAIN_MENU = State()
    SELECT_SUBJECT = State()
    SELECT_PRACTICE = State()
    MANAGE_QUEUE = State()
