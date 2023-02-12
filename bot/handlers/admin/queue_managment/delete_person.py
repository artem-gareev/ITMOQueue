from aiogram import types
from aiogram.dispatcher import FSMContext

from database import crud
from loader import dp, bot
from states.admin import AdminEditQueueStates
from swtichers import AdminSwitchers
from view import buttons, messages, keyboards

from config import settings


@dp.message_handler(text=buttons.delete_from_queue, state=AdminEditQueueStates.MAIN_MENU, user_id=settings.ADMINS_IDS)
async def switch_to_deleting_person(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        practice_id = data['practice_id']

    persons = crud.get_persons_for_practice(practice_id)
    queue = [[person.id, crud.get_user(person.user_id).name] for person in persons]
    await AdminEditQueueStates.SELECT_PERSON_TO_DELETE.set()
    await message.answer(messages.CHOOSE_PERSON_TO_DELETE, reply_markup=keyboards.back)
    msg = await message.answer(messages.LIST_OF_PERSONS, reply_markup=keyboards.select_person(queue))
    async with state.proxy() as data:
        data['list_id'] = msg.message_id


@dp.message_handler(text=buttons.back, state=AdminEditQueueStates.SELECT_PERSON_TO_DELETE, user_id=settings.ADMINS_IDS)
async def back_from_deleting_person(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        msg_id = data['list_id']
    try:
        await bot.delete_message(message.from_user.id, msg_id)
    except:
        pass
    await AdminSwitchers.manage_queue(message, state)


@dp.callback_query_handler(text_startswith="person_",
                           state=AdminEditQueueStates.SELECT_PERSON_TO_DELETE,
                           user_id=settings.ADMINS_IDS)
async def deleting_person(query: types.CallbackQuery, state: FSMContext):
    person_id = int(query.data.split("_")[-1])
    person = crud.get_person_for_practice_by_id(person_id)

    crud.drop_from_queue(person.user_id, person.practice_id)
    crud.move_queue(person.practice_id, person.priority, person.num_in_order, -1)

    await query.message.delete()
    await query.message.answer(messages.QUEUE_EDITED)
    await AdminSwitchers.manage_queue_from_query(query, state)
