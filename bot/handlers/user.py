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


@dp.callback_query_handler(text_startswith="practice_", state=UserStates.SELECT_PRACTICE)
async def switch_to_subject(query: types.CallbackQuery, state: FSMContext):
    await query.message.answer("IN_DEV")


@dp.message_handler(text=buttons.back, state=UserStates.SELECT_PRACTICE)
async def back_from_select_subject(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        message_id = data["list_id"]
    try:
        await bot.delete_message(message.from_user.id, message_id)
    except Exception:
        pass
    await UserSwitchers.select_subject(message, state, message.from_user.id)

# await queue_management(query.from_user.id, queue_id)
#
#
# @dp.message_handler(text=buttons.back, state=UserStates.MANAGE_QUEUE)
# async def back_from_switch_to_queue(message: types.Message, state: FSMContext):
#     await select_queue(message, state)
#
#
# @dp.message_handler(text=buttons.enter_queue, state=UserStates.MANAGE_QUEUE)
# async def enter_queue(message: types.Message, state: FSMContext):
#     async with state.proxy() as data:
#         queue_id = data['queue_id']
#     if message.from_user.id in [person.id for person in crud.get_queue_persons(queue_id)]:
#         await message.answer(messages.ALREADY_IN_QUEUE)
#         return
#     crud.get_in_queue(message.from_user.id, queue_id)
#     await message.answer(messages.GOT_IN_QUEUE)
#     await queue_management(message.from_user.id, queue_id)
#
#
# @dp.message_handler(text=buttons.leave_queue, state=UserStates.MANAGE_QUEUE)
# async def leave_queue(message: types.Message, state: FSMContext):
#     logger.info("start droping")
#     async with state.proxy() as data:
#         queue_id = data['queue_id']
#     logger.info(f"{message.from_user.id=}, {queue_id=}")
#     logger.info(crud.drop_from_queue(message.from_user.id, queue_id))
#     await queue_management(message.from_user.id, queue_id)
