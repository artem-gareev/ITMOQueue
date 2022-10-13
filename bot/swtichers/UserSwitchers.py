from datetime import datetime

from aiogram import types
from aiogram.dispatcher import FSMContext

from config import settings
from database import crud
from loader import bot
from states.user import UserStates
from view import keyboards, messages


async def main_menu(message: types.Message):
    await UserStates.MAIN_MENU.set()
    await message.answer(messages.IN_MAIN_MENU, reply_markup=keyboards.main_menu)

# async def queue_management(user_id, queue_id):
#     await UserStates.MANAGE_QUEUE.set()
#     persons = sort_persons(crud.get_persons_for_practice(queue_id))
#     persons = [person.user_id for person in persons if not person.is_left]
#     queue = crud.get_queue(queue_id)
#     kb = keyboards.queue_control_menu(user_id in persons, user_id in settings.ADMINS_IDS)
#     text = f"Очередь: {queue.name}\nЛюди в очереди:\n\n"
#     if not persons:
#         text += "Пока пусто..."
#         await bot.send_message(user_id, text, reply_markup=kb)
#         return
#
#     for i, person in enumerate(persons):
#         user = crud.get_user(person)
#         if user.telegram_id == user_id:
#             text += f"<b>{i + 1}. {user.name}</b>\n"
#         else:
#             text += f"{i + 1}. {user.name}\n"
#
#     await bot.send_message(user_id, text, reply_markup=kb)
#
#
# def sort_persons(persons: list[PersonsForPractice]):
#     result_dict = {}
#     today = datetime.now().strftime("%Y-%M-%d")
#     for person in persons:
#         if person.user_id not in result_dict.keys():
#             result_dict[person.user_id] = 0
#         if not person.is_left:
#             continue
#
#         if person.enter_date.strftime("%Y-%M-%d") == today:
#             result_dict[person.user_id] = 2
#             continue
#         if result_dict[person.user_id] != 2:
#             result_dict[person.user_id] = 1
#
#     return sorted(persons, key=lambda x: (result_dict[x.user_id], x.enter_date))
