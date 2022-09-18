from aiogram import types
from database import crud
from loader import bot
from states.user import UserStates
from view import keyboards, messages


async def main_menu(message: types.Message):
    await UserStates.MAIN_MENU.set()
    await message.answer(messages.IN_MAIN_MENU, reply_markup=keyboards.user_main_menu)


async def queue_management(user_id, queue_id):
    await UserStates.MANAGE_QUEUE.set()
    persons = [person.user_id for person in crud.get_queue_persons(queue_id)]

    kb = keyboards.queue_control_menu(user_id in persons)

    text = "Люди в очереди:\n\n"
    if not persons:
        text += "Пока пусто..."
        await bot.send_message(user_id, text, reply_markup=kb)
        return

    for i, person in enumerate(persons):
        user = crud.get_user(person)
        if user.telegram_id == user_id:
            text += f"<b>{i + 1}. {user.name}</b>\n"
        else:
            text += f"{i + 1}. {user.name}\n"

    await bot.send_message(user_id, text, reply_markup=kb)
