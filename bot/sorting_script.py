import time
from datetime import datetime


from database import crud


def sort_queues():
    practices = sum([crud.get_all_practices_for_subject(sbj.id) for sbj in crud.get_all_subjects()], [])
    for practice in practices:
        persons = crud.get_persons_for_practice(practice.id)
        persons = sorted(persons, key=lambda person: (person.is_new, person.enter_time))
        for i, person in enumerate(persons):
            crud.edit_user_priority(person.id, 0)
            crud.edit_user_order_place(person.id, i + 1)


if __name__ == '__main__':
    while True:
        if datetime.now().hour == 22 and datetime.now().minute == 40:
            sort_queues()
            time.sleep(60)
        time.sleep(5)
