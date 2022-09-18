import os

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

ADMINS_IDS = list(map(int, os.getenv("ADMINS_IDS").split(",")))

ROOT_PATH = os.getcwd()

DATABASE_PATH = os.path.join(ROOT_PATH, os.getenv("DATABASE_PATH"))
REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = os.getenv("REDIS_PORT")
