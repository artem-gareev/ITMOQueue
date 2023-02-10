from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import dp, bot, logger
from states.user import UserStates
from swtichers import UserSwitchers
from view import buttons


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
