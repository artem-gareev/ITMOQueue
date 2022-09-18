from aiogram import types
from aiogram.dispatcher import FSMContext
from database import crud
from loader import dp, bot
from states.admin import AdminStates
from states.user import UserStates
from swtichers import AdminSwitchers, UserSwitchers
from swtichers.UserSwitchers import queue_management
from view import buttons, keyboards, messages

from config import settings


@dp.message_handler(commands=["start"], state="*")
async def start_from_registration(message: types.Message):
    try:
        crud.create_user(message.from_user.id, "@" + message.from_user.username)
    except Exception:
        pass
    await UserSwitchers.main_menu(message)


@dp.message_handler(text=buttons.queues, state=[AdminStates.MAIN_MENU, UserStates.MAIN_MENU])
async def select_queue(message: types.Message, state: FSMContext):
    await UserStates.SELECT_QUEUE.set()
    queues = crud.get_all_queues()
    if not queues:
        await message.answer(messages.NO_QUEUES)
        return

    await message.answer(messages.SELECT_QUEUE, reply_markup=keyboards.back)
    msg = await message.answer(messages.LIST_OF_QUEUE, reply_markup=keyboards.queues_kb(queues))
    async with state.proxy() as data:
        data["list_id"] = msg.message_id


@dp.message_handler(text=buttons.back, state=UserStates.SELECT_QUEUE)
async def start_from_registration(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        message_id = data["list_id"]
    try:
        await bot.delete_message(message.from_user.id, message_id)
    except Exception:
        pass

    if message.from_user.id in settings.ADMINS_IDS:
        await AdminSwitchers.main_menu(message)
    else:
        await UserSwitchers.main_menu(message)


@dp.callback_query_handler(text_startswith="queue_", state=UserStates.SELECT_QUEUE)
async def choose_payment_method(query: types.CallbackQuery, state: FSMContext):
    await query.message.delete()
    queue_id = int(query.data.split("_")[-1])
    async with state.proxy() as data:
        data['queue_id'] = queue_id
    await queue_management(query.from_user.id, queue_id)


@dp.message_handler(text=buttons.back, state=UserStates.MANAGE_QUEUE)
async def start_from_registration(message: types.Message, state: FSMContext):
    await select_queue(message, state)


@dp.message_handler(text=buttons.enter_queue, state=UserStates.MANAGE_QUEUE)
async def enter_queue(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        queue_id = data['queue_id']
    if message.from_user.id in [person.id for person in crud.get_queue_persons(queue_id)]:
        await message.answer(messages.ALREADY_IN_QUEUE)
        return
    crud.get_in_queue(message.from_user.id, queue_id)
    await message.answer(messages.GOT_IN_QUEUE)
    await queue_management(message.from_user.id, queue_id)


@dp.message_handler(text=buttons.leave_queue, state=UserStates.MANAGE_QUEUE)
async def leave_queue(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        queue_id = data['queue_id']
    crud.drop_from_queue(message.from_user.id, queue_id)
    await queue_management(message.from_user.id, queue_id)
