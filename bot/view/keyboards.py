from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup,
                           KeyboardButton, ReplyKeyboardMarkup)
from database.models import Subject, PracticeTeacher
from view import buttons

main_menu = ReplyKeyboardMarkup(resize_keyboard=True)
main_menu.add(KeyboardButton(buttons.queues))

mange_subject = ReplyKeyboardMarkup(resize_keyboard=True)
mange_subject.add(KeyboardButton(buttons.add_subject))
mange_subject.add(KeyboardButton(buttons.delete_subject))
mange_subject.add(KeyboardButton(buttons.back))

mange_practice = ReplyKeyboardMarkup(resize_keyboard=True)
mange_practice.add(KeyboardButton(buttons.add_practice))
mange_practice.add(KeyboardButton(buttons.delete_practice))
mange_practice.add(KeyboardButton(buttons.back))

back = ReplyKeyboardMarkup(resize_keyboard=True)
back.add(KeyboardButton(buttons.back))


def subjects_kb(subjects: list[Subject]):
    kb = InlineKeyboardMarkup()
    for subject in subjects:
        kb.add(InlineKeyboardButton(subject.name, callback_data=f"subject_{subject.id}"))
    return kb


def practice_kb(practices: list[PracticeTeacher]):
    kb = InlineKeyboardMarkup()
    for practice in practices:
        kb.add(InlineKeyboardButton(practice.name, callback_data=f"practice_{practice.id}"))
    return kb


def queue_control_menu(in_queue: bool, is_admin: bool):
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    if in_queue:
        kb.add(buttons.leave_queue)
    else:
        kb.add(buttons.enter_queue)
    if is_admin:
        kb.add(buttons.move_queue)
    kb.add(buttons.back)
    return kb
