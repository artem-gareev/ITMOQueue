from aiogram import types
from aiogram.dispatcher import FSMContext

from database import crud
from loader import dp
from states.admin import AdminMainStates
from states.user import UserStates
from swtichers import AdminSwitchers
from view import buttons, messages

from config import settings


# @dp.message_handler(commands=["start"], state="*", user_id=settings.ADMINS_IDS)
# async def start_from_registration(message: types.Message):
#     try:
#         crud.create_user(message.from_user.id, "@" + message.from_user.username)
#     except Exception:
#         pass
#     await AdminSwitchers.main_menu(message)
#
#
# @dp.message_handler(text=buttons.add_queue, state=AdminMainStates.MAIN_MENU, user_id=settings.ADMINS_IDS)
# async def start_from_registration(message: types.Message):
#     await AdminSwitchers.send_queue_name(message)
#
#
# @dp.message_handler(text=buttons.back, state=AdminMainStates.SEND_QUEUE_NAME, user_id=settings.ADMINS_IDS)
# async def start_from_registration(message: types.Message):
#     await AdminSwitchers.main_menu(message)
#
#
# @dp.message_handler(content_types=["text"], state=AdminMainStates.SEND_QUEUE_NAME, user_id=settings.ADMINS_IDS)
# async def start_from_registration(message: types.Message):
#     crud.create_queue(message.text)
#     await message.answer(messages.QUEUE_SAVED)
#     await AdminSwitchers.main_menu(message)
#
#
# @dp.message_handler(text=buttons.move_queue, state=UserStates.MANAGE_QUEUE, user_id=settings.ADMINS_IDS)
# async def move_queue(message: types.Message,state:FSMContext):
#     await AdminSwitchers.move_queue(message,state)
