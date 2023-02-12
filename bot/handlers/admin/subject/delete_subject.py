from aiogram import types
from aiogram.dispatcher import FSMContext

from database import crud
from loader import dp, bot
from states.admin import AdminMainStates
from states.user import UserStates
from swtichers import AdminSwitchers, UserSwitchers
from view import buttons

from config import settings


@dp.message_handler(text=buttons.delete_subject, state=UserStates.SELECT_SUBJECT, user_id=settings.ADMINS_IDS)
async def switch_to_delete_subject(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        try:
            await bot.delete_message(message.from_user.id, data['list_id'])
        except Exception:
            pass

    await AdminSwitchers.send_subject_name_to_delete(message, state)


@dp.message_handler(text=buttons.back, state=AdminMainStates.SEND_SUBJECT_TO_DELETE, user_id=settings.ADMINS_IDS)
async def back_from_delete_subject(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        try:
            await bot.delete_message(message.from_user.id, data['list_id'])
        except Exception:
            pass

    await UserSwitchers.select_subject(message, state, message.from_user.id)


@dp.callback_query_handler(text_startswith="subject_", state=AdminMainStates.SEND_SUBJECT_TO_DELETE)
async def delete_subject(query: types.CallbackQuery, state: FSMContext):
    subject_id = int(query.data.split("_")[-1])
    crud.delete_subject(subject_id)
    await UserSwitchers.select_subject(query.message, state, query.from_user.id)
    await query.message.delete()
