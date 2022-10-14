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


async def select_subject(message: types.Message, state: FSMContext, user_id: int):
    subjects = crud.get_all_subjects()
    await UserStates.SELECT_SUBJECT.set()

    kb = keyboards.mange_subject if user_id in settings.ADMINS_IDS else keyboards.back
    text = messages.LIST_OF_SUBJECT if subjects else messages.NO_SUBJECTS
    await message.answer(messages.SELECT_SUBJECT, reply_markup=kb)
    msg = await message.answer(text, reply_markup=keyboards.subjects_kb(subjects))

    async with state.proxy() as data:
        data["list_id"] = msg.message_id


async def select_practice(message, state, user_id):
    async with state.proxy() as data:
        subject_id = data["subject_id"]

    await UserStates.SELECT_PRACTICE.set()
    practises = crud.get_all_practices_for_subject(subject_id)

    kb = keyboards.mange_practice if user_id in settings.ADMINS_IDS else keyboards.back
    text = messages.LIST_OF_PRACTICES if practises else messages.NO_PRACTISES

    await message.answer(messages.SELECT_PRACTICES, reply_markup=kb)
    msg = await message.answer(text, reply_markup=keyboards.practice_kb(practises))

    async with state.proxy() as data:
        data["list_id"] = msg.message_id

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
