from aiogram import types

from database import crud
from loader import dp
from swtichers import UserSwitchers


@dp.message_handler(commands=["start"], state="*")
async def start(message: types.Message):
    try:
        crud.create_user(message.from_user.id, "@" + message.from_user.username)
    except Exception:
        pass
    await UserSwitchers.main_menu(message)
