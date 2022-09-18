import os

from dotenv import load_dotenv
from pydantic import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    BOT_TOKEN: str
    ADMINS_IDS: list[int]
    ROOT_PATH = os.getcwd()

    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int

    REDIS_HOST: str
    REDIS_PORT: int

    class Config:
        @classmethod
        def parse_env_var(cls, field_name: str, raw_val: str):
            if field_name == 'ADMINS_IDS':
                return [int(x) for x in raw_val.split(',') if x]
            return cls.json_loads(raw_val)


settings = Settings()
