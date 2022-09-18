from aiogram import types

from bot import config
from loader import dp
from database import crud
from swtichers import AdminSwitchers
from view import buttons
from view import messages
from states.admin import AdminStates


@dp.message_handler(commands=["start"], state="*", user_id=config.ADMINS_IDS)
async def start_from_registration(message: types.Message):
    try:
        crud.create_user(message.from_user.id, "@" + message.from_user.username)
    except Exception:
        pass
    await AdminSwitchers.main_menu(message)


@dp.message_handler(text=buttons.add_queue, state=AdminStates.MAIN_MENU, user_id=config.ADMINS_IDS)
async def start_from_registration(message: types.Message):
    await AdminSwitchers.send_queue_name(message)


@dp.message_handler(text=buttons.back, state=AdminStates.SEND_QUEUE_NAME, user_id=config.ADMINS_IDS)
async def start_from_registration(message: types.Message):
    await AdminSwitchers.main_menu(message)


@dp.message_handler(content_types=["text"], state=AdminStates.SEND_QUEUE_NAME, user_id=config.ADMINS_IDS)
async def start_from_registration(message: types.Message):
    crud.create_queue(message.text)
    await message.answer(messages.QUEUE_SAVED)
    await AdminSwitchers.main_menu(message)
