from aiogram import types
from aiogram.dispatcher import FSMContext

from database import crud
from loader import dp
from states.admin import AdminMainStates
from states.user import UserStates
from swtichers import AdminSwitchers, UserSwitchers
from view import buttons, messages

from config import settings



@dp.message_handler(text=buttons.add_practice, state=UserStates.SELECT_PRACTICE, user_id=settings.ADMINS_IDS)
async def add_new_practice(message: types.Message):
    await AdminSwitchers.send_practice_name(message)


@dp.message_handler(text=buttons.back, state=AdminMainStates.SEND_PRACTICE_NAME, user_id=settings.ADMINS_IDS)
async def back_from_add_practice(message: types.Message, state: FSMContext):
    await UserSwitchers.select_practice(message, state, message.from_user.id)


@dp.message_handler(content_types=types.ContentTypes.TEXT, state=AdminMainStates.SEND_PRACTICE_NAME,
                    user_id=settings.ADMINS_IDS)
async def add_practice(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        subject_id = data["subject_id"]
    crud.create_practice(message.text, subject_id)
    await message.answer(messages.PRACTICE_SAVED)
    await UserSwitchers.select_practice(message, state, message.from_user.id)


