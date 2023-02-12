from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup,
                           KeyboardButton, ReplyKeyboardMarkup)
from database.models import Subject, PracticeTeacher
from view import buttons

main_menu = ReplyKeyboardMarkup(resize_keyboard=True)
main_menu.add(KeyboardButton(buttons.queues))
main_menu.add(KeyboardButton(buttons.questions))

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
        kb.add(buttons.manage_queue)

    kb.add(buttons.back)
    return kb


edit_queue = ReplyKeyboardMarkup(resize_keyboard=True)
edit_queue.add(KeyboardButton(buttons.delete_from_queue))
edit_queue.add(KeyboardButton(buttons.skip_person))
edit_queue.add(KeyboardButton(buttons.back))


def select_person(persons: list):
    kb = InlineKeyboardMarkup()
    for person in persons:
        kb.add(InlineKeyboardButton(person[1], callback_data=f"person_{person[0]}"))
    return kb


choose_purpose = ReplyKeyboardMarkup(resize_keyboard=True)
choose_purpose.row(KeyboardButton(buttons.new_lab), KeyboardButton(buttons.finish_questions))
choose_purpose.add(KeyboardButton(buttons.back))
