from aiogram import types
from aiogram.dispatcher import FSMContext

from database import crud
from loader import dp
from states.admin import AdminEditQueueStates
from states.user import UserStates
from swtichers import AdminSwitchers, UserSwitchers
from view import buttons, messages

from config import settings


@dp.message_handler(text=buttons.manage_queue, state=UserStates.MANAGE_QUEUE, user_id=settings.ADMINS_IDS)
async def switch_to_add_subject(message: types.Message, state: FSMContext):
    await AdminSwitchers.manage_queue(message, state)


@dp.message_handler(text=buttons.back, state=AdminEditQueueStates.MAIN_MENU, user_id=settings.ADMINS_IDS)
async def back_from_add_subject(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        practice_id = data['practice_id']
        subject_id = data["subject_id"]
    await UserStates.MANAGE_QUEUE.set()
    await UserSwitchers.queue_management(subject_id, practice_id, message.from_user.id)