from aiogram import types
from aiogram.dispatcher import FSMContext

import utils
from database import crud
from states.admin import AdminMainStates, AdminEditQueueStates
from swtichers import UserSwitchers
from view import keyboards, messages


async def send_subject_name(message: types.Message):
    await AdminMainStates.SEND_SUBJECT_NAME.set()
    await message.answer(messages.SEND_SUBJECT_NAME, reply_markup=keyboards.back)


async def send_practice_name(message: types.Message):
    await AdminMainStates.SEND_PRACTICE_NAME.set()
    await message.answer(messages.SEND_PRACTICE_NAME, reply_markup=keyboards.back)


async def send_subject_name_to_delete(message: types.Message, state: FSMContext):
    subjects = crud.get_all_subjects()
    if not subjects:
        return message.answer(messages.NO_SUBJECTS_TO_DELETE)

    await AdminMainStates.SEND_SUBJECT_TO_DELETE.set()
    await message.answer(messages.SEND_SUBJECT_NAME_TO_DELETE, reply_markup=keyboards.back)
    msg = await message.answer(messages.LIST_OF_SUBJECT, reply_markup=keyboards.subjects_kb(subjects))
    async with state.proxy() as data:
        data["list_id"] = msg.message_id


async def send_practice_name_to_delete(message: types.Message, state: FSMContext, subject_id: int):
    practice = crud.get_all_practices_for_subject(subject_id)
    if not practice:
        return message.answer(messages.NO_PRACTICES_TO_DELETE)

    await AdminMainStates.SEND_PRACTICE_TO_DELETE.set()
    await message.answer(messages.SEND_PRACTICE_NAME_TO_DELETE, reply_markup=keyboards.back)
    msg = await message.answer(messages.LIST_OF_PRACTICES, reply_markup=keyboards.practice_kb(practice))
    async with state.proxy() as data:
        data["list_id"] = msg.message_id


async def manage_queue(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        practice_id = data["practice_id"]
        subject_id = data["subject_id"]
    persons = crud.get_persons_for_practice(practice_id)
    text = utils.get_queue_text(subject_id, practice_id, persons, message.from_user.id)
    await message.answer(messages.IN_EDIT_QUEUE_MENU.format(queue=text), reply_markup=keyboards.edit_queue)
    await AdminEditQueueStates.MAIN_MENU.set()


async def manage_queue_from_query(query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        practice_id = data["practice_id"]
        subject_id = data["subject_id"]
    persons = crud.get_persons_for_practice(practice_id)
    text = utils.get_queue_text(subject_id, practice_id, persons, query.from_user.id)
    await query.message.answer(messages.IN_EDIT_QUEUE_MENU.format(queue=text), reply_markup=keyboards.edit_queue)
    await AdminEditQueueStates.MAIN_MENU.set()

