from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup,
                           KeyboardButton, ReplyKeyboardMarkup)
from database.models import Queue
from view import buttons

admin_main_menu = ReplyKeyboardMarkup(resize_keyboard=True)
admin_main_menu.add(KeyboardButton(buttons.queues))
admin_main_menu.add(KeyboardButton(buttons.add_queue))

user_main_menu = ReplyKeyboardMarkup(resize_keyboard=True)
user_main_menu.add(KeyboardButton(buttons.queues))

back = ReplyKeyboardMarkup(resize_keyboard=True)
back.add(KeyboardButton(buttons.back))


def queues_kb(queues: list[Queue]):
    kb = InlineKeyboardMarkup()
    for queue in queues:
        kb.add(InlineKeyboardButton(queue.name, callback_data=f"queue_{queue.id}"))
    return kb


def queue_control_menu(in_queue: bool):
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    if in_queue:
        kb.add(buttons.leave_queue)
    else:
        kb.add(buttons.enter_queue)
    kb.add(buttons.back)
    return kb
