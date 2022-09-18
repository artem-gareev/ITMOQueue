from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from database.database import create_database
from handlers import dp
from loader import logger


async def on_startup(dispatcher: Dispatcher):
    logger.info("Started")
    create_database()
    logger.info("db created")


async def on_shutdown(dispatcher: Dispatcher):
    await dispatcher.storage.close()
    await dispatcher.storage.wait_closed()


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown)
