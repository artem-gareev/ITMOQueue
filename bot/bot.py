from aiogram.utils import executor
from loader import dp
from aiogram.dispatcher import Dispatcher
from database.database import create_database


async def on_startup(dispatcher: Dispatcher):
    print("Started")
    create_database()
    print("db maked")

async def on_shutdown(dispatcher: Dispatcher):
    await dispatcher.storage.close()
    await dispatcher.storage.wait_closed()


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown)
