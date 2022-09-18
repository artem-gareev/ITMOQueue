from aiogram.dispatcher.filters.state import State, StatesGroup


class AdminStates(StatesGroup):
    MAIN_MENU = State()
    SEND_QUEUE_NAME = State()