from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import dp
from states.user import UserStates
from swtichers import UserSwitchers
from view import buttons


@dp.message_handler(text=buttons.queues, state=UserStates.MAIN_MENU)
async def queues(message: types.Message, state: FSMContext):
    await UserSwitchers.select_subject(message, state, message.from_user.id)


@dp.message_handler(text=buttons.lab_questions, state=UserStates.MAIN_MENU)
async def questions(message: types.Message, state: FSMContext):
    await message.answer("В разработке")
