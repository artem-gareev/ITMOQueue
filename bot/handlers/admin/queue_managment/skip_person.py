from aiogram import types
from aiogram.dispatcher import FSMContext

from database import crud
from loader import dp, bot
from states.admin import AdminEditQueueStates
from swtichers import AdminSwitchers
from view import buttons, messages, keyboards

from config import settings


@dp.message_handler(text=buttons.skip_person, state=AdminEditQueueStates.MAIN_MENU, user_id=settings.ADMINS_IDS)
async def switch_to_deleting_person(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        practice_id = data['practice_id']

    persons = crud.get_persons_for_practice(practice_id)
    if len(persons) < 2:
        await message.answer(messages.CANT_SKIP)
        return
    person_to_skip = persons[0]
    person_to_push = persons[1]
    if person_to_push.priority != person_to_skip.priority:
        await message.answer(messages.DIFFERENT_PRIORITES)
        return

    crud.edit_user_order_place(person_to_skip.id, 2)
    crud.edit_user_order_place(person_to_push.id, 1)

    await message.answer(messages.QUEUE_EDITED)
    await AdminSwitchers.manage_queue(message, state)
