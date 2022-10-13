from aiogram.dispatcher.filters.state import State, StatesGroup


class AdminMainStates(StatesGroup):
    SEND_SUBJECT_NAME = State()
    SEND_PRACTICE_NAME = State()


class AdminEditQueueStates(StatesGroup):
    MAIN_MENU = State()
    SEND_TO_SWAP_FROM = State()
    SEND_TO_SWAP_TO = State()
    SEND_PRACTICE_NAME_TO_ADD = State()
    SEND_PRACTICE_NAME_TO_DELETE = State()
