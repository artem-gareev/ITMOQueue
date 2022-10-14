from aiogram import types
from aiogram.dispatcher import FSMContext

from database import crud
from states.admin import AdminMainStates
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
