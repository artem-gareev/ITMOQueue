from aiogram import types
from aiogram.dispatcher import FSMContext

from database import crud
from loader import dp
from states.admin import AdminMainStates
from states.user import UserStates
from swtichers import AdminSwitchers, UserSwitchers
from view import buttons, messages

from config import settings


@dp.message_handler(text=buttons.add_subject, state=UserStates.SELECT_SUBJECT, user_id=settings.ADMINS_IDS)
async def switch_to_add_subject(message: types.Message):
    await AdminSwitchers.send_subject_name(message)


@dp.message_handler(text=buttons.back, state=AdminMainStates.SEND_SUBJECT_NAME, user_id=settings.ADMINS_IDS)
async def back_from_add_subject(message: types.Message, state: FSMContext):
    await UserSwitchers.select_subject(message, state, message.from_user.id)


@dp.message_handler(content_types=types.ContentTypes.TEXT, state=AdminMainStates.SEND_SUBJECT_NAME,
                    user_id=settings.ADMINS_IDS)
async def add_subject(message: types.Message, state: FSMContext):
    crud.create_subject(message.text)
    await message.answer(messages.SUBJECT_SAVED)
    await UserSwitchers.select_subject(message, state, message.from_user.id)


