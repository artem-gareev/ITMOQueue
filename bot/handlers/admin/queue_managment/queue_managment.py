from aiogram import types
from aiogram.dispatcher import FSMContext

from database import crud
from loader import dp
from states.user import UserStates
from swtichers import UserSwitchers
from view import buttons, messages


@dp.message_handler(text=buttons.back, state=UserStates.MANAGE_QUEUE)
async def back_from_switch_to_queue(message: types.Message, state: FSMContext):
    await UserSwitchers.select_practice(message, state, message.from_user.id)


@dp.message_handler(text=buttons.enter_queue, state=UserStates.MANAGE_QUEUE)
async def enter_queue(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        practice_id = data['practice_id']
        subject_id = data["subject_id"]
    persons = crud.get_persons_for_practice(practice_id)
    all_persons_for_lab = sum(
        [crud.get_persons_for_practice(practice.id) for practice in crud.get_all_practices_for_subject(subject_id)],
        [])
    if message.from_user.id in [p.user_id for p in all_persons_for_lab]:
        await message.answer(messages.ALREADY_IN_QUEUE)
        return

    priority = crud.get_user_priority(message.from_user.id, practice_id)
    number_to_enter = max([0] + [person.num_in_order for person in persons if person.priority == priority]) + 1

    crud.enter_queue(message.from_user.id, practice_id, priority, number_to_enter)
    await message.answer(messages.GOT_IN_QUEUE)
    await UserStates.MANAGE_QUEUE.set()
    await UserSwitchers.queue_management(subject_id, practice_id, message.from_user.id)


@dp.message_handler(text=buttons.leave_queue, state=UserStates.MANAGE_QUEUE)
async def leave_queue(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        practice_id = data['practice_id']
        subject_id = data["subject_id"]

    person = crud.get_person_for_practice(practice_id, message.from_user.id)
    crud.drop_from_queue(telegram_id=person.user_id, practice_id=practice_id)
    crud.move_queue(practice_id, person.priority, person.num_in_order, -1)
    await message.answer(messages.LEFT_FROM_QUEUE)
    await UserStates.MANAGE_QUEUE.set()
    await UserSwitchers.queue_management(subject_id, practice_id, message.from_user.id)
