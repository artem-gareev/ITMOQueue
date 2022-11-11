from datetime import datetime

from aiogram import types
from aiogram.dispatcher import FSMContext

from utils import get_queue_text
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


async def queue_management(subject_id, practice_id, user_id):
    persons = [person.user_id for person in crud.get_persons_for_practice(practice_id)]
    text = get_queue_text(subject_id, practice_id, persons, user_id)
    await bot.send_message(user_id, text, reply_markup=keyboards.queue_control_menu(
        user_id in persons, user_id in settings.ADMINS_IDS
    ))
