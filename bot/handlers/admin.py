from aiogram import types
from aiogram.dispatcher import FSMContext

from database import crud
from loader import dp, bot
from states.admin import AdminMainStates
from states.user import UserStates
from swtichers import AdminSwitchers, UserSwitchers
from view import buttons, messages

from config import settings


@dp.message_handler(text=buttons.add_subject, state=UserStates.SELECT_SUBJECT, user_id=settings.ADMINS_IDS)
async def add_new_subject(message: types.Message):
    await AdminSwitchers.send_subject_name(message)


@dp.message_handler(text=buttons.back, state=AdminMainStates.SEND_SUBJECT_NAME, user_id=settings.ADMINS_IDS)
async def back_from_add_subject(message: types.Message, state: FSMContext):
    await UserSwitchers.select_subject(message, state, message.from_user.id)


@dp.message_handler(content_types=types.ContentTypes.TEXT, state=AdminMainStates.SEND_SUBJECT_NAME,
                    user_id=settings.ADMINS_IDS)
async def save_subject(message: types.Message, state: FSMContext):
    crud.create_subject(message.text)
    await message.answer(messages.SUBJECT_SAVED)
    await UserSwitchers.select_subject(message, state, message.from_user.id)


@dp.message_handler(text=buttons.add_practice, state=UserStates.SELECT_PRACTICE, user_id=settings.ADMINS_IDS)
async def add_new_practice(message: types.Message):
    await AdminSwitchers.send_practice_name(message)


@dp.message_handler(text=buttons.back, state=AdminMainStates.SEND_PRACTICE_NAME, user_id=settings.ADMINS_IDS)
async def back_from_add_practice(message: types.Message, state: FSMContext):
    await UserSwitchers.select_practice(message, state, message.from_user.id)


@dp.message_handler(content_types=types.ContentTypes.TEXT, state=AdminMainStates.SEND_PRACTICE_NAME,
                    user_id=settings.ADMINS_IDS)
async def save_practice(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        subject_id = data["subject_id"]
    crud.create_practice(message.text, subject_id)
    await message.answer(messages.PRACTICE_SAVED)
    await UserSwitchers.select_practice(message, state, message.from_user.id)


@dp.message_handler(text=buttons.delete_subject, state=UserStates.SELECT_SUBJECT, user_id=settings.ADMINS_IDS)
async def switch_to_delete_subject(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        try:
            await bot.delete_message(message.from_user.id, data['list_id'])
        except Exception:
            pass

    await AdminSwitchers.send_subject_name_to_delete(message, state)


@dp.callback_query_handler(text_startswith="subject_", state=AdminMainStates.SEND_SUBJECT_TO_DELETE)
async def delete_subject(query: types.CallbackQuery, state: FSMContext):
    subject_id = int(query.data.split("_")[-1])
    crud.delete_subject(subject_id)
    await UserSwitchers.select_subject(query.message, state, query.from_user.id)
    await query.message.delete()


@dp.message_handler(text=buttons.delete_practice, state=UserStates.SELECT_PRACTICE, user_id=settings.ADMINS_IDS)
async def switch_to_delete_practice(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        try:
            await bot.delete_message(message.from_user.id, data['list_id'])
        except Exception:
            pass
        await AdminSwitchers.send_practice_name_to_delete(message, state, data['subject_id'])


@dp.callback_query_handler(text_startswith="practice_", state=AdminMainStates.SEND_PRACTICE_TO_DELETE)
async def delete_practise(query: types.CallbackQuery, state: FSMContext):
    practice_id = int(query.data.split("_")[-1])
    crud.delete_practice(practice_id)
    await UserSwitchers.select_practice(query.message, state, query.from_user.id)
    await query.message.delete()


@dp.message_handler(text=buttons.back, state=AdminMainStates.SEND_SUBJECT_TO_DELETE, user_id=settings.ADMINS_IDS)
async def switch_from_delete_subject(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        try:
            await bot.delete_message(message.from_user.id, data['list_id'])
        except Exception:
            pass

    await UserSwitchers.select_subject(message, state, message.from_user.id)


@dp.message_handler(text=buttons.back, state=AdminMainStates.SEND_PRACTICE_TO_DELETE, user_id=settings.ADMINS_IDS)
async def switch_from_delete_subject(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        try:
            await bot.delete_message(message.from_user.id, data['list_id'])
        except Exception:
            pass

    await UserSwitchers.select_practice(message, state, message.from_user.id)

# @dp.message_handler(text=buttons.back, state=AdminMainStates.SEND_QUEUE_NAME, user_id=settings.ADMINS_IDS)
# async def start_from_registration(message: types.Message):
#     await AdminSwitchers.main_menu(message)
#
#
# @dp.message_handler(content_types=["t ext"], state=AdminMainStates.SEND_QUEUE_NAME, user_id=settings.ADMINS_IDS)
# async def start_from_registration(message: types.Message):
#     crud.create_queue(message.text)
#     await message.answer(messages.QUEUE_SAVED)
#     await AdminSwitchers.main_menu(message)
#
#
# @dp.message_handler(text=buttons.move_queue, state=UserStates.MANAGE_QUEUE, user_id=settings.ADMINS_IDS)
# async def move_queue(message: types.Message,state:FSMContext):
#     await AdminSwitchers.move_queue(message,state)
