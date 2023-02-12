from database import crud


def sort_queues():
    practices = sum([crud.get_all_practices_for_subject(sbj.id) for sbj in crud.get_all_subjects()], [])
    for practice in practices:
        persons = crud.get_persons_for_practice(practice)
        persons = sorted(persons, key=lambda person: (person.is_new, person.enter_time))
        for i, person in enumerate(persons):
            crud.edit_user_priority(person.id, 0)
            crud.edit_user_order_place(person.id, i + 1)


if __name__ == '__main__':
    sort_queues()
