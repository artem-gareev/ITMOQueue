from aiogram import types
from aiogram.dispatcher import FSMContext

from database import crud
from loader import dp, bot, logger
from states.admin import AdminMainStates
from states.user import UserStates
from swtichers import AdminSwitchers, UserSwitchers
from view import buttons, keyboards, messages

from config import settings


@dp.message_handler(commands=["start"], state="*")
async def start(message: types.Message):
    try:
        crud.create_user(message.from_user.id, "@" + message.from_user.username)
    except Exception:
        pass
    await UserSwitchers.main_menu(message)


@dp.message_handler(text=buttons.queues, state=UserStates.MAIN_MENU)
async def select_subjects(message: types.Message, state: FSMContext):
    await UserSwitchers.select_subject(message, state, message.from_user.id)


@dp.message_handler(text=buttons.back, state=UserStates.SELECT_SUBJECT)
async def back_from_select_subject(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        message_id = data["list_id"]
    try:
        await bot.delete_message(message.from_user.id, message_id)
    except Exception:
        pass
    await UserSwitchers.main_menu(message)


@dp.callback_query_handler(text_startswith="subject_", state=UserStates.SELECT_SUBJECT)
async def switch_to_practise(query: types.CallbackQuery, state: FSMContext):
    subject_id = int(query.data.split("_")[-1])
    async with state.proxy() as data:
        data["subject_id"] = subject_id
    await UserSwitchers.select_practice(query.message, state, query.from_user.id)
    await query.message.delete()


@dp.message_handler(text=buttons.back, state=UserStates.SELECT_PRACTICE)
async def back_from_select_subject(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        message_id = data["list_id"]
    try:
        await bot.delete_message(message.from_user.id, message_id)
    except Exception:
        pass
    await UserSwitchers.select_subject(message, state, message.from_user.id)


@dp.callback_query_handler(text_startswith="practice_", state=UserStates.SELECT_PRACTICE)
async def switch_to_subject(query: types.CallbackQuery, state: FSMContext):
    practice_id = int(query.data.split("_")[-1])
    async with state.proxy() as data:
        data["practice_id"] = practice_id
        subject_id = data["subject_id"]
    await query.message.delete()
    await UserStates.MANAGE_QUEUE.set()
    await UserSwitchers.queue_management(subject_id, practice_id, query.from_user.id)


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


@dp.message_handler(text=buttons.skip_ahead, state=UserStates.MANAGE_QUEUE)
async def enter_queue(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        practice_id = data['practice_id']
        subject_id = data["subject_id"]
    persons = crud.get_persons_for_practice(practice_id)
    logger.info([person.user_id for person in persons])
    for i in range(len(persons) - 1):
        logger.info(f"{i} {persons[i].user_id}")
        if persons[i].user_id == message.from_user.id:
            crud.edit_user_order_place(persons[i].user_id, practice_id, persons[i].num_in_order + 1)
            crud.edit_user_order_place(persons[i + 1].user_id, practice_id, persons[i].num_in_order - 1)
            break

    await message.answer(messages.PEOPLE_MOVED)
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
