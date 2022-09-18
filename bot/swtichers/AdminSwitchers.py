from aiogram import types
from states.admin import AdminStates
from view import keyboards, messages


async def main_menu(message: types.Message):
    await AdminStates.MAIN_MENU.set()
    await message.answer(messages.IN_MAIN_MENU, reply_markup=keyboards.admin_main_menu)


async def send_queue_name(message: types.Message):
    await AdminStates.SEND_QUEUE_NAME.set()
    await message.answer(messages.SEND_QUEUE_NAME, reply_markup=keyboards.back)
