from aiogram.dispatcher.filters.state import State, StatesGroup


class AdminMainStates(StatesGroup):
    SEND_SUBJECT_NAME = State()
    SEND_PRACTICE_NAME = State()
    SEND_SUBJECT_TO_DELETE = State()
    SEND_PRACTICE_TO_DELETE = State()


class AdminEditQueueStates(StatesGroup):
    MAIN_MENU = State()
    SELECT_PERSON_TO_DELETE = State()
