from aiogram import types
from aiogram.dispatcher import FSMContext

from database import crud
from loader import dp, bot
from states.admin import AdminMainStates, AdminEditQueueStates
from states.user import UserStates
from swtichers import AdminSwitchers, UserSwitchers
from view import buttons, messages, keyboards

from config import settings






@dp.message_handler(text=buttons.manage_queue,
                    state=UserStates.MANAGE_QUEUE,
                    user_id=settings.ADMINS_IDS)
async def switch_to_manage_subject(message: types.Message, state: FSMContext):
    await AdminSwitchers.manage_queue(message, state)


@dp.message_handler(text=buttons.back,
                    state=AdminEditQueueStates.MAIN_MENU,
                    user_id=settings.ADMINS_IDS)
async def switch_from_manage_subject(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        practice_id = data['practice_id']
        subject_id = data["subject_id"]

    await UserStates.MANAGE_QUEUE.set()
    await UserSwitchers.queue_management(subject_id, practice_id, message.from_user.id)


@dp.message_handler(text=buttons.skip_ahead,
                    state=AdminEditQueueStates.MAIN_MENU,
                    user_id=settings.ADMINS_IDS)
async def switch_from_manage_subject(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        practice_id = data['practice_id']

    persons = crud.get_persons_for_practice(practice_id)
    queue = [[person.id, crud.get_user(person.user_id).name] for person in persons]
    await AdminEditQueueStates.SEND_TO_SKIP_FROM.set()
    await message.answer(messages.CHOOSE_PERSON_TO_SKIP, reply_markup=keyboards.back)
    msg = await message.answer(messages.LIST_OF_PERSONS, reply_markup=keyboards.select_person(queue))
    async with state.proxy() as data:
        data['list_id'] = msg.message_id


@dp.message_handler(text=buttons.back,
                    state=[AdminEditQueueStates.SEND_TO_SKIP_FROM,
                           AdminEditQueueStates.SEND_TO_SWAP_FROM,
                           AdminEditQueueStates.SEND_TO_SWAP_TO],
                    user_id=settings.ADMINS_IDS)
async def back_to_main_edit_menu(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        msg_id = data['list_id']
    try:
        await bot.delete_message(message.from_user.id, msg_id)
    except:
        pass
    await AdminSwitchers.manage_queue(message, state)


@dp.callback_query_handler(text_startswith="person_",
                           state=AdminEditQueueStates.SEND_TO_SKIP_FROM,
                           user_id=settings.ADMINS_IDS)
async def move_forward(query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        practice_id = data['practice_id']
    person_id = int(query.data.split("_")[-1])
    person = crud.get_person_for_practice_by_id(person_id)
    crud.move_queue(practice_id, person.priority, person.num_in_order, -1)
    crud.move_queue(practice_id, 0, -1, 1)
    crud.edit_user_order_place(person.user_id, practice_id, 0)
    crud.edit_user_priority(person_id, 0)
    await query.message.delete()
    await query.message.answer(messages.QUEUE_EDITED)
    await AdminSwitchers.manage_queue_from_query(query, state)


@dp.message_handler(text=buttons.move_queue,
                    state=AdminEditQueueStates.MAIN_MENU,
                    user_id=settings.ADMINS_IDS)
async def move_queue(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        practice_id = data['practice_id']
    queue = crud.get_persons_for_practice(practice_id)
    crud.drop_from_queue(queue[0].user_id, practice_id)
    crud.move_queue(practice_id, queue[0].priority, 0, -1)
    await message.answer(messages.QUEUE_MOVED)
    await AdminSwitchers.manage_queue(message, state)


@dp.message_handler(text=buttons.manage_queue,
                    state=AdminEditQueueStates.MAIN_MENU,
                    user_id=settings.ADMINS_IDS)
async def select_to_swap_from(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        practice_id = data['practice_id']

    persons = crud.get_persons_for_practice(practice_id)
    queue = [[person.id, crud.get_user(person.user_id).name] for person in persons]
    await AdminEditQueueStates.SEND_TO_SWAP_FROM.set()
    await message.answer(messages.CHOOSE_PERSON_TO_SWAP_FROM, reply_markup=keyboards.back)
    msg = await message.answer(messages.LIST_OF_PERSONS, reply_markup=keyboards.select_person(queue))
    async with state.proxy() as data:
        data['list_id'] = msg.message_id


@dp.callback_query_handler(text_startswith="person_",
                           state=AdminEditQueueStates.SEND_TO_SWAP_FROM,
                           user_id=settings.ADMINS_IDS)
async def switch_from_manage_subject(query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        practice_id = data['practice_id']
        data['person_id'] = int(query.data.split("_")[-1])
        list_id = data['list_id']
    try:
        await bot.delete_message(query.from_user.id, list_id)
    except:
        pass

    persons = crud.get_persons_for_practice(practice_id)
    queue = [[person.id, crud.get_user(person.user_id).name] for person in persons]
    await AdminEditQueueStates.SEND_TO_SWAP_TO.set()
    msg = await query.message.answer(messages.CHOOSE_PERSON_TO_SWAP_TO, reply_markup=keyboards.select_person(queue))

    async with state.proxy() as data:
        data['list_id'] = msg.message_id
    await query.message.delete()


@dp.callback_query_handler(text_startswith="person_",
                           state=AdminEditQueueStates.SEND_TO_SWAP_TO,
                           user_id=settings.ADMINS_IDS)
async def switch_from_manage_subject(query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        practice_id = data['practice_id']
        list_id = data['list_id']
        swap_from = crud.get_person_for_practice_by_id(data['person_id'])
    try:
        await bot.delete_message(query.from_user.id, list_id)
    except:
        pass

    swap_to = crud.get_person_for_practice_by_id(int(query.data.split("_")[-1]))
    crud.move_queue(practice_id, swap_from.priority, swap_from.num_in_order, -1)
    crud.move_queue(practice_id, swap_to.priority, swap_to.num_in_order, 1)
    crud.edit_user_order_place(swap_from.user_id, practice_id, swap_to.num_in_order + 1)
    await query.message.answer(messages.QUEUE_EDITED)
    await AdminSwitchers.manage_queue_from_query(query, state)
