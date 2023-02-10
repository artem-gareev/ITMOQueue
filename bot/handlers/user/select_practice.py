from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import dp, bot, logger
from states.user import UserStates
from swtichers import UserSwitchers
from view import buttons


@dp.message_handler(text=buttons.back, state=UserStates.SELECT_PRACTICE)
async def back_from_select_practice(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        message_id = data["list_id"]
    try:
        await bot.delete_message(message.from_user.id, message_id)
    except Exception:
        pass
    await UserSwitchers.select_subject(message, state, message.from_user.id)


@dp.callback_query_handler(text_startswith="practice_", state=UserStates.SELECT_PRACTICE)
async def switch_to_manage_queue(query: types.CallbackQuery, state: FSMContext):
    practice_id = int(query.data.split("_")[-1])
    async with state.proxy() as data:
        data["practice_id"] = practice_id
        subject_id = data["subject_id"]
    await query.message.delete()
    await UserStates.MANAGE_QUEUE.set()
    await UserSwitchers.queue_management(subject_id, practice_id, query.from_user.id)
